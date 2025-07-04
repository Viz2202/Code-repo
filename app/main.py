from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse
import logging
import datetime

from .config import settings
from .webhook import webhook_router
from .github_client import github_client
from .analyzers.static_analyzers import StaticAnalyzer
from .firebase.firebase_database import Database
from .routes.user_routes import user_router
from .routes.repo_routes import repo_router
from .routes.pull_requests_routes import pull_request_router
from .routes.issues_router import Issues, issues_router

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
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(repo_router, prefix="/repos", tags=["repos"])
app.include_router(pull_request_router, prefix="/pull-requests", tags=["pull_requests"])
app.include_router(issues_router, prefix="/issues", tags=["issues"])

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
    if response.get("action") not in ["opened","synchronize", "reopened"]:
        return JSONResponse(content={"message": "ignored"}, status_code=200)
    allissues = StaticAnalyzer().analyze_files(response)
    print("Time is " + str(datetime.datetime.now()))
    Issues.set_data(allissues)
    return JSONResponse(content={"message": "ok"}, status_code=200)


@app.route("/get-data",methods=["GET"])
async def get_data(request: Request):
    try:
        data = Issues.get_data("issues")
        return JSONResponse(content=data, status_code=200)
    except Exception as e:
        logger.error(f"Error retrieving data: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving data")

