from fastapi import APIRouter, Request, HTTPException, Header
import hashlib
import hmac
import json
import logging
from typing import Optional

from .config import settings
from .github_client import github_client

logger = logging.getLogger(__name__)

webhook_router = APIRouter()

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """Verify GitHub webhook signature"""
    if not signature_header:
        return False
    
    try:
        sha_name, signature = signature_header.split('=')
        if sha_name != 'sha256':
            return False
        
        # Create HMAC signature
        mac = hmac.new(
            settings.WEBHOOK_SECRET.encode('utf-8'),
            msg=payload_body,
            digestmod=hashlib.sha256
        )
        
        return hmac.compare_digest(mac.hexdigest(), signature)
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return False

@webhook_router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: Optional[str] = Header(None),
    x_hub_signature_256: Optional[str] = Header(None)
):
    """Handle GitHub webhook events"""
    
    # Get raw payload
    payload_body = await request.body()
    
    # Verify signature
    if not verify_signature(payload_body, x_hub_signature_256):
        logger.warning("Invalid webhook signature")
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    # Parse JSON payload
    try:
        payload = json.loads(payload_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    logger.info(f"Received {x_github_event} event")
    
    # Handle different event types
    if x_github_event == "pull_request":
        return await handle_pull_request_event(payload)
    elif x_github_event == "ping":
        return await handle_ping_event(payload)
    else:
        logger.info(f"Ignoring {x_github_event} event")
        return {"status": "ignored", "event": x_github_event}

async def handle_ping_event(payload: dict):
    """Handle ping event (webhook test)"""
    logger.info("Ping event received - webhook is working!")
    return {"status": "pong", "message": "Webhook is working!"}

async def handle_pull_request_event(payload: dict):
    """Handle pull request events"""
    action = payload.get("action")
    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})
    
    repo_full_name = repo.get("full_name")
    pr_number = pr.get("number")
    pr_title = pr.get("title")
    
    logger.info(f"PR {action}: #{pr_number} '{pr_title}' in {repo_full_name}")
    
    # Only process certain actions
    if action in ["opened", "synchronize", "reopened"]:
        logger.info(f"Processing PR #{pr_number} for code review")
        
        # For now, just post a simple comment
        comment = f"🤖 **Code Review Bot Activated!**\n\nI'm analyzing your changes in PR #{pr_number}. This is Phase 1 - basic webhook handling is working!\n\n*More features coming soon...*"
        
        success = github_client.post_pr_comment(repo_full_name, pr_number, comment)
        
        if success:
            return {"status": "processed", "action": action, "pr": pr_number}
        else:
            return {"status": "error", "message": "Failed to post comment"}
    
    return {"status": "ignored", "action": action}
