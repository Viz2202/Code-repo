import requests
import os
import json
class GetFile:   
    def fetch_file(self,raw_url_and_patch):
        headers = {
            "Authorization": "Bearer " + os.getenv("GITHUB_TOKEN"),
            "Accept": "application/vnd.github.v3.raw"
        }

        patch_and_full_file = []
        for file in raw_url_and_patch:
            url= file.get("raw_url")

            full_file_response = requests.get(url, headers=headers)
            if full_file_response.status_code == 200:
                file_text = full_file_response.text
                patch_and_full_file.append((file.get("patch"), file_text))
            else:
                print("Failed to fetch file:", full_file_response.status_code)
                break

        return patch_and_full_file
