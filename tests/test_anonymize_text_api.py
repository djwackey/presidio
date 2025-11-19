from fastapi import status
from fastapi.testclient import TestClient

headers = {}


def test_text_anonymize(client: TestClient):
    text = "张三，男，45岁。电话：13800138000。诊断结果：高血压。"
    payload = {"text": text}
    request_url = "/anonymize"
    response = client.post(request_url, json=payload, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    print(f"[response_json] {response_json}")
