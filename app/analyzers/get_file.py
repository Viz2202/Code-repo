import requests
import os
class GetFile:
    def fetch_file(self, file_path:str):
        print(file_path)
        url = "https://raw.githubusercontent.com/Viz2202/test/main/" + file_path
        headers = {
            "Authorization": "Bearer " + os.getenv("GITHUB_TOKEN"),
            "Accept": "application/vnd.github.v3.raw"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            file_text = response.text
            return file_text # or process it however you like
        else:
            print("Failed to fetch file:", response.status_code)

