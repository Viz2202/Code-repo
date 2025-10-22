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
    password = login_user.password
    email = login_user.email
    user_details_ref = db.collection('users').where('email', '==', email)
    doc = user_details_ref.get()

    if not doc:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    user_data = doc[0].to_dict()
    stored_hash= user_data["password"]
    if not bcrypt.checkpw(password.encode('utf-8'),stored_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access"
        )
    return user_data
        

@login_router.post("/signup")
def signup(user: Signup):
    check_user = db.collection('users').where("email" ,"==" ,user.emailid)
    check_doc = check_user.get()
    if check_doc:
        return {"message":False}
    else:
        user_id = str(uuid.uuid4())
        user_details_ref = db.collection('users').document(user_id)
        hash_password = user.password.encode('utf-8')
        hash_password = bcrypt.hashpw(hash_password,bcrypt.gensalt())
        user_details_ref.set({
            "name": user.name,
            "email": user.emailid,
            "github_username": user.github_username,
            "password": hash_password,
            "user_id": user_id
        })
        return {"message":True}