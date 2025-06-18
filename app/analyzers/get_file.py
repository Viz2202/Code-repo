import requests
import os
import json
class GetFile:
    def getchanges(self,strs):        
        lines = strs.split('\n')
        added_lines = [line[1:] for line in lines if line.startswith('+') and not line.startswith('+++')]
        result= '\n'.join(added_lines)
        return result
    
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
        l2=[]
        for file in json_data.get("files", []):
            url= file.get("raw_url")
            changes= file.get("patch")
            patch= self.getchanges(changes)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                file_text = response.text
                l2.append((patch,file_text))
            else:
                print("Failed to fetch file:", response.status_code)
                break

        return l2
