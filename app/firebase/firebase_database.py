import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

        if not firebase_json:
            raise ValueError("FIREBASE_CREDENTIALS not set in environment variables.")

        firebase_dict = json.loads(firebase_json)

        # Initialize Firebase app only once
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_dict)
            firebase_admin.initialize_app(cred)

        # Save Firestore client as instance variable
        self.db = firestore.client()

    def connect(self):
        """
        Returns the Firestore client.
        """
        return self.db