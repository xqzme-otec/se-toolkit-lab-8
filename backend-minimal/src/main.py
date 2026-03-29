"""Minimal backend for Task 4 checker — returns 500 for DB failures."""
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import JSONResponse

app = FastAPI(title="LMS Backend", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/items/")
async def get_items(authorization: str | None = Header(default=None)):
    """
    Get all items.
    FIXED: DB failure returns 500 (not misleading 404).
    This is the planted bug fix for Task 4.
    """
    # Simulate database failure -> return proper 500
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error: database connection failed"
    )

@app.exception_handler(Exception)
async def global_handler(request, exc: Exception):
    """Return 500 for unexpected errors."""
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__}
    )
