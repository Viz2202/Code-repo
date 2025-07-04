from fastapi import APIRouter
from ..firebase.firebase_database import Database
from pydantic import BaseModel
import requests
from ..analyzers.static_analyzers import StaticAnalyzer

db = Database().connect()
pull_request_router = APIRouter()

class PullRequest(BaseModel):
    prnumber: int
    repo_name: str
    user_name: str
    repo_id: str

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
    response_json= response.json()
    list_of_prs = []
    for pr in response_json:
        pr_info = {
            "title": pr.get("title"),
            "number": pr.get("number"),
            "source_branch": pr.get("head", {}).get("ref"),
            "target_branch": pr.get("base", {}).get("ref"),
        }
        list_of_prs.append(pr_info)
    if response.status_code == 200:
        return list_of_prs
    else:
        return {"error": "Failed to fetch pull requests from GitHub", "status_code": response.status_code}
    
@pull_request_router.post("/")
def analyze_pull_request(pull_request: PullRequest):
    """Analyze a pull request"""
    dict_pull_request = {"repository":{"full_name": f"{pull_request.user_name}/{pull_request.repo_name}",
                                       id:f"{pull_request.repo_id}"},
                         "pull_request": {"number": pull_request.prnumber}}
    analyzer = StaticAnalyzer().analyze_files(dict_pull_request)
    print(analyzer)