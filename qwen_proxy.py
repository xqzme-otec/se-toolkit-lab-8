from fastapi import FastAPI
import uvicorn
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/chat/completions")
async def chat(request: dict):
    try:
        response = client.chat.completions.create(
            model=request.get("model", "qwen/qwen3-coder:free"),
            messages=request.get("messages", [])
        )
        return {"choices": [{"message": {"content": response.choices[0].message.content}}]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=42005)
