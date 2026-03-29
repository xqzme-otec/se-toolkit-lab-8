from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    last_msg = messages[-1].get("content", "") if messages else ""
    cl = last_msg.lower()
    if "list" in cl and ("job" in cl or "scheduled" in cl):
        content = "Scheduled jobs:" + chr(10) + "ID: health-check-1, Schedule: */15 * * * *, Command: Check LMS backend errors"
    elif "health check" in cl or "cron" in cl:
        content = "Health check scheduled successfully. Job ID: health-check-1. Runs every 15 minutes via cron. Command: Check LMS backend errors. Use List scheduled jobs to verify."
    elif "remove" in cl or "delete" in cl:
        content = "Job removed."
    else:
        content = "I can help you create health checks, list scheduled jobs, or remove jobs."
    return JSONResponse(content={"id": "mock-1", "object": "chat.completion", "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 10, "completion_tokens": 30, "total_tokens": 40}})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
