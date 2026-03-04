from fastapi import APIRouter,HTTPException
from ..firebase.firebase_database import Database
from pydantic import BaseModel
import requests

db = Database().connect()
repo_router = APIRouter()

class Repo(BaseModel):
    repo_id: str
    repo_name: str
    user_id: str
    platform: str

def get_github_repos(username):
    github_url=f"https://api.github.com/users/{username}/repos?per_page=100"
    github_response = requests.get(github_url)
    if github_response.status_code!=200:
        return []
    return github_response.json()

def get_gitlab_repos(user_id):
    gitlab_repo_url = f"https://gitlab.com/api/v4/users/{user_id}/projects?visibility=public&per_page=100"
    gitlab_response = requests.get(gitlab_repo_url)
    if gitlab_response.status_code!=200:
        return []
    return gitlab_response.json()

def get_gitlab_repos_via_username(username):
    gitlab_url=f"https://gitlab.com/api/v4/users?username={username}"
    response = requests.get(gitlab_url)
    if response.status_code!=200:
        return []
    data = response.json()
    if not data:
        return []
    else:
        user_id = data[0]['id']
        return get_gitlab_repos(user_id)
    
def simplify_github(repo):
    return{
        "id":repo["id"],
        "name":repo["name"],
        "platform":"github"
    }

def simplify_gitlab(repo):
    return{
        "id":repo["id"],
        "name":repo["name"],
        "platform":"gitlab"
    }

@repo_router.get("/all-remote/{user_id}")
def get_all_remote_repos(user_id):
    """Get all remote repositories"""
    user = db.collection('users').document(user_id).get()
    user_info = user.to_dict()
    github_user_name = user_info.get('github_username')
    gitlab_user_name = user_info.get('gitlab_username')
    github_repos = get_github_repos(github_user_name)
    gitlab_repos = get_gitlab_repos_via_username(gitlab_user_name)
    combined = []
    combined.extend(simplify_github(r) for r in github_repos)
    combined.extend(simplify_gitlab(r) for r in gitlab_repos)
    return combined

@repo_router.delete("/remove/{repo_id}")
def remove_repo(repo_id):
    try:
        repo_ref = db.collection('repos').document(repo_id)
        if repo_ref.get().exists:
            repo_ref.delete()
            print("Route Hit")
            return {"message":"Repo deleted successfully"}
        else:
            raise HTTPException(status=404,detail="repo not found")
    except Exception as e:
        raise HTTPException(status=500,detail=str(e))

@repo_router.get("/{user_id}")
def get_repos(user_id):
    """Get all repositories"""
    repo_details_ref = db.collection('repos').where('user_id', '==', user_id)
    docs = repo_details_ref.stream()
    repos = {doc.id: doc.to_dict() for doc in docs}
    return repos

@repo_router.post("/")
def add_repo(repo: Repo):
    """Add a new repository"""
    repo_details_ref = db.collection('repos').document(repo.repo_id+"_"+repo.platform)
    repo_details_ref.set(repo.dict())
    return {"message": "Repository added successfully", "repo_id": repo.repo_id}
