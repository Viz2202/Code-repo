from fastapi import APIRouter, HTTPException, status
from ..firebase.firebase_database import Database
from pydantic import BaseModel
import requests
from ..analyzers.static_analyzers import StaticAnalyzer
from .issues_router import Issues
import uuid
import bcrypt

db = Database().connect()
login_router = APIRouter()

class Login(BaseModel):
    email: str
    password: str

class Signup(BaseModel):
    name: str
    emailid: str
    password: str
    github_username: str

class UserOut(BaseModel):
    name: str
    email: str
    github_username: str
    password: str
    user_id: str

@login_router.post("")
def login(login_user: Login):
    """Get all pull requests for a repository"""
    user_details_ref = db.collection('users').where('email', '==', login_user.email).where('password', '==', login_user.password)
    doc = user_details_ref.get()
    print(doc)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access"
        )
    for user in doc:
        return user.to_dict()
        

@login_router.post("/signup")
def signup(user: Signup):
    user_id = str(uuid.uuid4())
    user_details_ref = db.collection('users').document(user_id)
    user_details_ref.set({
        "name": user.name,
        "email": user.emailid,
        "github_username": user.github_username,
        "password": user.password,
        "user_id": user_id
    })
    return "Registered successfully"