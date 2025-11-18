FROM python:3.12.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Chinese spaCy model
RUN python -m spacy download zh_core_web_sm && \
    python -m spacy download zh_core_web_lg

COPY . .

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
