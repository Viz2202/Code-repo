from fastapi import APIRouter
from ..firebase.firebase_database import Database
from pydantic import BaseModel
import uuid

db = Database().connect()
user_router = APIRouter()

class User(BaseModel):
    name: str
    email: str
    github_username: str
    password: str

class UserOut(BaseModel):
    name: str
    email: str
    github_username: str
    password: str
    user_id: str

@user_router.get("/")
def hello():
    """Hello World endpoint"""
    return {"message": "Hello, World!"}

@user_router.get("/{user_id}")
def get_user(user_id):
    """Get all registered users"""
    user_details_ref = db.collection('users').document(user_id)
    doc = user_details_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return data
    else:
        return "Document not found."

@user_router.post("/")
def set_user(user: User):
    user_id = str(uuid.uuid4())
    user_details_ref = db.collection('users').document(user_id)
    user_details_ref.set({
        "name": user.name,
        "email": user.email,
        "github_username": user.github_username,
        "password": user.password,
        "user_id": user_id
    })
    return UserOut(
        name=user.name,
        email=user.email,
        github_username=user.github_username,
        password=user.password,
        user_id=user_id
    )

@user_router.post("/register")
def register_user(name: str):
    return {"message": f"User {name} registered successfully"}
