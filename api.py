import json
import os
import time
from contextlib import asynccontextmanager
from io import BytesIO

import fitz  # PyMuPDF
import openai
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator

from chinese_anonymizer.anonymizer import ChineseAnonymizer
from logger import log, loggers

load_dotenv()

LOG_PATH = os.getenv("LOG_PATH")
LOG_LEVEL = os.getenv("LOG_LEVEL")
PROJECT_NAME = os.getenv("PROJECT_NAME")

# Initialize the Chinese anonymizer
anonymizer = ChineseAnonymizer()


def extract_text_from_pdf(contents: bytes) -> str:
    """Extract text from PDF file using PyMuPDF (extensible for future file types)"""
    try:
        doc = fitz.open(stream=BytesIO(contents), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF text extraction failed: {str(e)}")


# Extensible file type mapping: add new extractors here for other file types
FILE_EXTRACTORS = {
    ".pdf": extract_text_from_pdf,
    # Future examples:
    # ".docx": extract_text_from_docx,
    # ".txt": extract_text_from_plaintext
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await anonymizer.init()
    yield


app = FastAPI(title="Medical Data De-identification API", lifespan=lifespan)

loggers.init_config(PROJECT_NAME, LOG_PATH, LOG_LEVEL)


class AnonymizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="脱敏文本不能为空")

    @field_validator("text")
    def not_blank(cls, v):
        if not v.strip():
            raise ValueError("脱敏文本不能为空或仅包含空格")
        return v


class AnonymizeResponse(BaseModel):
    original_text: str
    anonymized_text: str
    detected_entities: list


@app.post("/anonymize", response_model=AnonymizeResponse)
async def anonymize_text(request: AnonymizeRequest, background_tasks: BackgroundTasks):
    # 定义要匿名化的实体和替换的标签
    try:
        start_time = time.perf_counter()
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

        # await validate_and_store(request.text, anonymized_result.text, detected_entities)
        background_tasks.add_task(validate_and_store, request.text, anonymized_result.text, detected_entities)
        elapsed_time = round(time.perf_counter() - start_time, 4)
        return AnonymizeResponse(
            elapsed_time=elapsed_time,
            original_text=request.text,
            anonymized_text=anonymized_result.text,
            detected_entities=detected_entities,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/anonymize-pdf")
async def anonymize_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Anonymize PDF file content and return as text stream"""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        # Read PDF content
        contents = await file.read()
        doc = fitz.open(stream=BytesIO(contents), filetype="pdf")

        # Extract text from all pages
        text = ""
        for page in doc:
            text += page.get_text() + "\n"

        log.info(f"[original_text] {text}")

        # Anonymize the text
        anonymized_result = anonymizer.anonymize_text(
            text=text,
            anonymize_entities=anonymizer.anonymize_entities,
        )

        # Extract detected entities for response
        detected_entities = []
        for result in anonymizer.analyze(text):
            detected_entities.append(
                {
                    "entity_type": result.entity_type,
                    "text": text[result.start : result.end],
                    "start": result.start,
                    "end": result.end,
                    "score": round(result.score, 2),
                }
            )

        log.info(f"[anonymized_result] {anonymized_result.text}")
        background_tasks.add_task(validate_and_store, text, anonymized_result.text, detected_entities)

        # Create a BytesIO stream for the response
        output = BytesIO()
        output.write(anonymized_result.text.encode("utf-8"))
        output.seek(0)

        # Return as streaming response
        return StreamingResponse(
            output,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename=anonymized_{file.filename.replace('.pdf', '.txt')}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


async def validate_and_store(original_text: str, anonymized_text: str, detected_entities: list):
    """Validate anonymized text using OpenAI and store results in database"""
    try:
        # Initialize OpenAI client
        client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))

        # Create validation prompt
        prompt = f"""你的任务是对比以下两段文本，判断匿名化处理是否完全成功。

请仔细检查匿名化后的文本中，是否仍然存在任何可能识别个人身份的信息（PII），包括但不限于姓名、地址、电话号码、身份证号、邮箱、账号信息、组织名称或其他可关联个体的细节。

请严格只根据文本内容进行判断，不进行推测或补全。

请以 JSON 格式返回结果，结构如下：
{{
  "pii_leak_detected": True 或 False,
  "description": "若为 True，请简要说明发现的可能PII线索；若为 False，请说明匿名化看起来完整无误。",
  "evidence_snippets": ["列出可疑文本片段，如无则为空数组"]
}}

原始文本如下：
{original_text}

匿名化后的文本如下：
{anonymized_text}"""

        # Call OpenAI API
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME"),
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

    uvicorn.run(app, host="0.0.0.0", port=9000)
