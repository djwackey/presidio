import os
import inspect
import tempfile
import fitz  # PyMuPDF

from fastapi.testclient import TestClient


def test_anonymize_pdf(client: TestClient):
    font_name = "SimSun"
    font_path = "/usr/share/fonts/simsun.ttc"

    # Create a test PDF file with sample text containing PII
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        doc = fitz.open()
        page = doc.new_page()
        text = "张三的电话号码是13800138000，身份证号是110101199001011234"
        page.insert_text((50, 50), text, fontname=font_name, fontfile=font_path, fontsize=14)

        doc.save(temp_pdf.name)
        doc.close()

    try:
        # Upload the test PDF
        with open(temp_pdf.name, "rb") as f:
            response = client.post("/anonymize-pdf", files={"file": ("test.pdf", f, "application/pdf")})

        # Check response status code
        assert response.status_code == 200

        # Check that the response is a streaming response
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]

        # Get the anonymized text
        anonymized_text = response.text
        print(f"[anonymized_text] {anonymized_text}")

        # Check that PII has been anonymized
        assert "张三" not in anonymized_text
        assert "13800138000" not in anonymized_text
        assert "110101199001011234" not in anonymized_text

        # Check that anonymized placeholders are present
        assert "<NAME>" in anonymized_text
        assert "<PHONE>" in anonymized_text
        assert "<ID_CARD>" in anonymized_text

    finally:
        # Clean up the temporary file
        os.unlink(temp_pdf.name)


if __name__ == "__main__":
    test_anonymize_pdf()
    print("Test passed successfully!")
