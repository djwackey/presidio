import asyncio
import json

import httpx


async def anonymize_text():
    request_url = "http://127.0.0.1:8000/anonymize"
    text = "患者李明，联系电话：15912345678"
    data = json.dumps({"text": text}, ensure_ascii=False)
    result = {}
    headers = {"Content-Type": "application/json"}
    print(f"[request_url] {request_url}")
    print(f"[request_data] {data}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                request_url, data=data, headers=headers, timeout=15.0
            )
            print(f"[status_code] {response.status_code}")
            response.raise_for_status()
            resp_text = response.json()
            print(f"[response_text] {resp_text}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP错误: {e}")
        except httpx.RequestError as e:
            print(f"请求失败: {e}")
        except ValueError as e:
            print(f"JSON解析错误: {e}")
    return result


if __name__ == "__main__":
    asyncio.run(anonymize_text())
