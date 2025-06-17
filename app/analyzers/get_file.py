import requests
import os
import json
class GetFile:
    def fetch_file(self,commit_id:str):
        #url = "https://raw.githubusercontent.com/Viz2202/test/main/" + file_path + "?ref=" + commit_id 
        url_2="https://api.github.com/repos/Viz2202/test/commits/" + commit_id
        headers = {
            "Authorization": "Bearer " + os.getenv("GITHUB_TOKEN"),
            "Accept": "application/vnd.github.v3.raw"
        }
        #response = requests.get(url, headers=headers)
        response2 = requests.get(url_2, headers=headers)
        json_data = json.loads(response2.text)        
        #print(json_data.get("files"))

        list1= []
        for file in json_data.get("files", []):
            url= file.get("raw_url")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                file_text = response.text
                list1.append(file_text) # or process it however you like
            else:
                print("Failed to fetch file:", response.status_code)
                break
        return list1
