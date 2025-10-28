from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chinese_anonymizer.anonymizer import ChineseAnonymizer

app = FastAPI(title="Medical Data De-identification API")

# Initialize the Chinese anonymizer
anonymizer = ChineseAnonymizer()


class AnonymizeRequest(BaseModel):
    text: str


class AnonymizeResponse(BaseModel):
    original_text: str
    anonymized_text: str
    detected_entities: list


@app.post("/anonymize", response_model=AnonymizeResponse)
async def anonymize_text(request: AnonymizeRequest):
    # 定义要匿名化的实体和替换的标签
    anonymize_entities = {
        "PERSON": "<NAME>",
        "ADDRESS": "<ADDRESS>",
        "ID_CARD": "<ID_CARD>",
        "PHONE_NUMBER": "<PHONE>",
        "INPATIENT_NO": "<INPATIENT>",
        "OUTPATIENT_NO": "<OUTPATIENT>",
        "PAYMENT_AMOUNT": "<PAYMENT>",
    }
    try:
        # Analyze and anonymize the text
        anonymized_result = anonymizer.anonymize_text(
            text=request.text,
            anonymize_entities=anonymize_entities,
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

        return AnonymizeResponse(
            original_text=request.text, anonymized_text=anonymized_result.text, detected_entities=detected_entities
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
