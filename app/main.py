from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
import datetime

from .config import settings
from .webhook import webhook_router
from .github_client import github_client
from .analyzers.static_analyzers import StaticAnalyzer
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate configuration on startup
try:
    settings.validate()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Automated Code Review Bot for GitHub Pull Requests"
)

# Include webhook router
app.include_router(webhook_router, prefix="/webhook", tags=["webhook"])

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": f"{settings.APP_NAME} is running",
        "version": settings.VERSION,
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test GitHub API connectivity
        user = github_client.get_user()
        return {
            "status": "healthy",
            "github_connection": "ok",
            "github_user": user.login,
            "timestamp": "2024-01-01T00:00:00Z"  # You can add actual timestamp
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.route("/webhook", methods=["POST"])
async def github_webhook(request: Request):
    # handle the webhook
    response = await request.json()
    allissues = StaticAnalyzer().analyze_files(response)
    print("Time is " + str(datetime.datetime.now()))
    print(f"Analyzed issues: {allissues}")
    return JSONResponse(content={"message": "ok"}, status_code=200)

