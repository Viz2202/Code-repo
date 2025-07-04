from ..firebase.firebase_database import Database
from google.cloud import firestore
from fastapi import APIRouter

issues_router = APIRouter()

class Issues:
    def set_data(issuelist: list):
        """
        Set issue data in the Firebase database.
        :param issuelist: List of issues to be stored.
        """
        db = Database().connect()
        safe_id = f"{issuelist[0]['repoid']}_{issuelist[0]['pull_request_number']}_{issuelist[0]['time']}"
        doc_ref = db.collection("issues").document(safe_id)
        list1=[]
        for item in issuelist:
            # Assuming item is a dictionary with 'file', 'issues', etc.
            list1.append({
                "file": item['file'],
                "issues": item['issues'],
            })
        doc_ref.set({"issuelist":list1})
    
    def get_data(repo_id: str, pull_request_number: int):
        """
        Get issue data from the Firebase database.
        :return: List of issues.
        """
        db = Database().connect()
        issues_ref =db.collection('issues').where('__name__', '>=', db.collection('issues').document(f'{repo_id}_{pull_request_number}_')).where('__name__', '<', db.collection('issues').document(f'{repo_id}_{pull_request_number}_\uf8ff'))
        docs = issues_ref.stream()
        issues = []
        for doc in docs:
            issues.append(doc.to_dict())
        return issues

@issues_router.get("/{repo_id}_{pull_request_number}")
def get_issues(repo_id: str, pull_request_number: int):
    """
    Get all issues from the database.
    :return: List of issues.
    """
    issues = Issues.get_data(repo_id, pull_request_number)
    return {"issues": issues}