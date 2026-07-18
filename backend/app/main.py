from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router

app = FastAPI(
    title="Elite Cynical CMO Campaign Strategy API",
    description="Asynchronous production-grade backend for the Cynical CMO campaign generator.",
    version="1.0.0"
)

# Configure CORS middleware explicitly listing allowed origins with credentials enabled to resolve browser console blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include consolidated routes directly without prefix
app.include_router(api_router)

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify backend status.
    """
    return {"status": "healthy"}
