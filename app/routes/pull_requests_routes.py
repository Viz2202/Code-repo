from fastapi import APIRouter
from ..firebase.firebase_database import Database
from pydantic import BaseModel
import requests

db = Database().connect()
pull_request_router = APIRouter()

class PullRequest(BaseModel):
    prnumber: int
    repo_id: str
    pr_status: str
    info: list

@pull_request_router.get("/{repo_id}")
def get_pull_requests(repo_id: str):
    """Get all pull requests for a repository"""
    pr_details_ref = db.collection('pull_requests').where('repo_id', '==', repo_id)
    docs = pr_details_ref.stream()
    pull_requests = {doc.id: doc.to_dict() for doc in docs}
    return pull_requests

@pull_request_router.get("/all-remote/{repo_id}")
def get_all_remote_pull_requests(repo_id: str): 
    """Get all remote pull requests for a repository"""
    repo_details = db.collection('repos').document(repo_id).get().to_dict()
    user_id = repo_details.get('user_id')
    user_details_ref = db.collection('users').document(user_id).get().to_dict()
    user_name = user_details_ref.get('github_username')
    repo_name = repo_details.get('repo_name')
    github_url = f"https://api.github.com/repos/{user_name}/{repo_name}/pulls"
    response = requests.get(github_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch pull requests from GitHub", "status_code": response.status_code}
    
@pull_request_router.post("/")
def add_pull_request(pull_request: PullRequest):
    """Add a new pull request"""
    pr_details_ref = db.collection('pull_requests').document(f"{pull_request.repo_id}_{pull_request.prnumber}")
    pr_details_ref.set(pull_request.dict())
    return {"message": "Pull request added successfully", "pr_id": f"{pull_request.repo_id}_{pull_request.prnumber}"}