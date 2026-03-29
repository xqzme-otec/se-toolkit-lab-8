from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items/")
def items():
    raise HTTPException(status_code=500, detail="Internal server error: database connection failed")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
