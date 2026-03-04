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
        safe_id = f"{issuelist[0]['repoid']}_{issuelist[0]['pull_request_number']}_{issuelist[0]['platform']}_{issuelist[0]['time']}"
        doc_ref = db.collection("issues").document(safe_id)
        time = issuelist[0]['time']
        repoid = issuelist[0]['repoid']
        pr = issuelist[0]['pull_request_number']
        platform = issuelist[0]['platform']
        list1=[]
        for item in issuelist:
            # Assuming item is a dictionary with 'file', 'issues', etc.
            list1.append({
                "file": item['file'],
                "issues": item['issues'],
            })
        doc_ref.set({"platform":platform,"repo_id": repoid,"pr_number": pr,"timestamp": time,"issuelist": list1})
    
    def get_data(repo_id: str, pull_request_number: str,platform: str):
        db = Database().connect()

        issues_ref = (
            db.collection("issues")
            .where("repo_id", "==", repo_id)
            .where("pr_number", "==", int(pull_request_number))
            .where("platform","==",platform)
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .limit(1)
        )

        docs = issues_ref.stream()
        latest_issuelist = []

        for doc in docs:
            latest_issuelist = doc.to_dict().get("issuelist", [])
            break
        return [{"issuelist":latest_issuelist}]
    
    def get_id(repo_id: str, pull_request_number: str,platform: str):
        """
        Get issue data from the Firebase database.
        :return: List of issues.
        """
        db = Database().connect()
        issues_ref =db.collection('issues').where('__name__', '>=', db.collection('issues').document(f'{repo_id}_{pull_request_number}_{platform}')).where('__name__', '<', db.collection('issues').document(f'{repo_id}_{pull_request_number}_{platform}_\uf8ff'))
        docs = issues_ref.stream()
        document_id = []
        for doc in docs:
            document_id.append(doc.id)
        
        return document_id


@issues_router.get("/{repo_id}_{pull_request_number}_{platform}")
def get_issues(repo_id: str, pull_request_number: str,platform: str):
    """
    Get all issues from the database.
    :return: List of issues.
    """
    issues = Issues.get_data(repo_id, pull_request_number,platform)
    return {"issues": issues}

@issues_router.get("/ids/{repo_id}_{pull_request_number}_{platform}")
def get_id(repo_id: str, pull_request_number: str,platform: str):
    ids = Issues.get_id(repo_id, pull_request_number,platform)
    return {"ids": ids}