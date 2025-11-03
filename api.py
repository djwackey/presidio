from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import openai
import json
import os

from chinese_anonymizer.anonymizer import ChineseAnonymizer

# Initialize the Chinese anonymizer
anonymizer = ChineseAnonymizer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await anonymizer.init()
    yield


app = FastAPI(title="Medical Data De-identification API", lifespan=lifespan)


class AnonymizeRequest(BaseModel):
    text: str


class AnonymizeResponse(BaseModel):
    original_text: str
    anonymized_text: str
    detected_entities: list


@app.post("/anonymize", response_model=AnonymizeResponse)
async def anonymize_text(request: AnonymizeRequest, background_tasks: BackgroundTasks):
    # 定义要匿名化的实体和替换的标签
    try:
        # Analyze and anonymize the text
        anonymized_result = anonymizer.anonymize_text(
            text=request.text,
            anonymize_entities=anonymizer.anonymize_entities,
        )

        # Extract detected entities for response
        detected_entities = []
        for result in anonymizer.analyze(request.text):
            detected_entities.append(
                {
                    "entity_type": result.entity_type,
                    "text": request.text[result.start : result.end],
                    "start": result.start,
                    "end": result.end,
                    "score": round(result.score, 2),
                }
            )

        background_tasks.add_task(validate_and_store, request.text, anonymized_result.text, detected_entities)
        return AnonymizeResponse(
            original_text=request.text, anonymized_text=anonymized_result.text, detected_entities=detected_entities
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def validate_and_store(original_text: str, anonymized_text: str, detected_entities: list):
    """Validate anonymized text using OpenAI and store results in database"""
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Create validation prompt
        prompt = f"""Check if the following text contains any personally identifiable information (PII) that should have been removed during anonymization. The original text was anonymized to remove names, phone numbers, ID numbers, addresses, and medical records. Respond with a JSON object containing 'contains_pii': boolean and 'identified_pii': array of strings with any detected PII elements.

Anonymized text: {anonymized_text}"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a PII validation assistant. Respond ONLY with valid JSON."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        openai_result = json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"OpenAI validation failed: {str(e)}")
        return

    # Store results in database
    from chinese_anonymizer.db_connector import DatabaseConnector

    try:
        db = DatabaseConnector()
        await db.add_validation_result(original_text, anonymized_text, openai_result, detected_entities)
        await db.close()
    except Exception as e:
        print(f"Database storage failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
