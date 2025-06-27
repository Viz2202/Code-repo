import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("./coderepo-214e5-firebase-adminsdk-fbsvc-b64e726eea.json") 
firebase_admin.initialize_app(cred)
db = firestore.client()

class Database:
    def __init__(self):
        pass

    def connect(self):
        # Logic to connect to the Firebase Realtime Database
        pass

    def get_data(self, path: str):
        # Logic to retrieve data from the specified path
        pass

    def set_data(self, issuelist: list):
        for item in issuelist:
            # Assuming item is a dictionary with 'file', 'issues', etc.
            safe_id = f"{item['repoid']}_{item['time']}"
            doc_ref = db.collection("issues").document(safe_id)

            doc_ref.set({
                "file": item['file'],
                "issues": item['issues'],
                "repo_name": item['repo_name'],
                "pull_request_number": item['pull_request_number'],
                "repoid": item['repoid'],
                "time": item['time']
            })
    def update_data(self, path: str, data: dict):
        # Logic to update data at the specified path
        pass

    def delete_data(self, path: str):
        # Logic to delete data at the specified path
        pass