from fastapi import APIRouter
from ..firebase.firebase_database import Database
from pydantic import BaseModel
import requests

db = Database().connect()
repo_router = APIRouter()

class Repo(BaseModel):
    repo_id: str
    repo_name: str
    user_id: str

@repo_router.get("/{user_id}")
def get_repos(user_id):
    """Get all repositories"""
    repo_details_ref = db.collection('repos').where('user_id', '==', user_id)
    docs = repo_details_ref.stream()
    repos = {doc.id: doc.to_dict() for doc in docs}
    return repos


@repo_router.get("/all-remote/{user_id}")
def get_all_remote_repos(user_id):
    """Get all remote repositories"""
    user_name = db.collection('users').document(user_id).get().to_dict().get('github_username')
    github_url=f"https://api.github.com/users/{user_name}/repos"
    github_public_repo = requests.get(github_url).json()
    return github_public_repo

@repo_router.post("/")
def add_repo(repo: Repo):
    """Add a new repository"""
    repo_details_ref = db.collection('repos').document(repo.repo_id)
    repo_details_ref.set(repo.dict())
    return {"message": "Repository added successfully", "repo_id": repo.repo_id}