# -*- coding: utf-8 -*-
import json
import requests
import re

from urllib.parse import urljoin


API_VERSION = "/api/v1/"

# memos类
class Memos:

    def __init__(self, content:str, resourceIdList = [], relationList = [], visibility:str = "PRIVATE", filePath = [], fileUrl = []):
        self.content = content
        self.visibility = visibility
        self.resourceIdList = resourceIdList
        self.relationList = relationList
        self.filePath = filePath
        self.fileUrl = fileUrl

    def get_tags(self):
        reg = r"\#[^\s]+"
        return re.findall(reg, self.content)

    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, 
    #         sort_keys=True, indent=4)
    
# memos相关API
class Memos_api:

    def __init__(self, openId, openapi_url):
        self.openId = openId
        self.openapi_url = openapi_url

    def create_memo(self, memos:Memos):

        if memos.filePath:
            for file in memos.filePath:
                res = self.upload_file(file)

                if res:
                    memos.resourceIdList.append(res)
        
        if memos.fileUrl:
            for file in memos.fileUrl:
                res = self.create_resource(file)

                if res:
                    memos.resourceIdList.append(res)
        
        tags = memos.get_tags()
        if len(tags):
            for tag in tags:
                self.create_tag(tag)

        url = urljoin(self.openapi_url, API_VERSION + "memo")
        # url = self.openapi_url + "memo"
        headers = {"Content-Type": "application/json"}
        params = {"openId" : self.openId}
        data = { "content": memos.content, "visibility": memos.visibility, "resourceIdList": memos.resourceIdList, "relationList": memos.relationList}

        try:
            res = requests.post(url, json=data, headers=headers, params=params)

            match res.status_code:
                case 200:
                    print(200, "Created memo", json.loads(res.text)["content"])
                    return True
                case 400:
                    print(400, "Invalid request")
                    return False
                case 401:
                    print(401, "Unauthorized")
                    return False
                case 403:
                    print(403, "Forbidden to create public memo")
                    return False
                case 500:
                    print(500, "Internal server error")
                    return False
                case _:
                    print("Unknown error")
                    return False
        except Exception as e:
            print("create memo error:", e)
            return False
        

    def create_tag(self, tag):
        url = urljoin(self.openapi_url, API_VERSION + "tag")
        # url = self.openapi_url + "tag"
        headers = {"Content-Type": "application/json"}
        params = {"openId" : self.openId}
        data = {"name": tag.replace("#", "")}

        try:
            
            res = requests.post(url, json=data, headers=headers, params=params)
            
            match res.status_code:
                case 200:
                    print(200, "Created tag", res.text)
                    return True
                case 400:
                    print(400, "Invalid request")
                    return False
                case 500:
                    print(500, "Internal server error")
                    return False
                case _:
                    print("Unknown error")
                    return False

        except Exception as e:
            print("create tag error:", e)
            return None
    
    # 上传文件
    # {
    #   "id": 123,
    #   "filename": "example.png"
    #   // other fields
    # }
    def upload_file(self, filePath):
        url = urljoin(self.openapi_url, API_VERSION + "resource/blob")
        # url = self.openapi_url + "resource/blob"
        params = {"openId" : self.openId}

        if filePath.split(".")[-1] == "png":
            content_type = "image/png"
        elif filePath.split(".")[-1] == "jpg":
            content_type = "image/jpeg"
        elif filePath.split(".")[-1] == "jpeg":
            content_type = "image/jpeg"
        elif filePath.split(".")[-1] == "gif":
            content_type = "image/gif"
        elif filePath.split(".")[-1] == "mp4":
            content_type = "video/mpeg4"
        elif filePath.split(".")[-1] == "mp3":
            content_type = "audio/mp3"
        else:
            print("unknown file type")
            content_type = ""

        try:
            files = {'file': (filePath.split("/")[-1], open(filePath, 'rb'), str(content_type))}

            res = requests.post(url, files=files, params=params)

            match res.status_code:
                case 200:
                    json_data = json.loads(res.text)
                    print(200, "OK 上传文件", json_data["filename"])
                    return json_data["id"]
                case 400:
                    print(400, "Invalid request")
                    return None
                case 401:
                    print(401, "Unauthorized")
                    return None
                case 413:
                    print(413, "File too large")
                    return None
                case 500:
                    print(500, "Internal server error")
                    return None
                case _:
                    print("Unknown error")
                    return None
                
        except Exception as e:
            print("upload file error:", e)
            return None
    
    # 创建资源
    def create_resource(self, fileUrl):
        url = urljoin(self.openapi_url, API_VERSION + "resource")
        # url = self.openapi_url + "resource"
        headers = {"Content-Type": "application/json"}
        data = {
            "filename" : fileUrl.split("/")[-1],
            "externalLink": fileUrl
        }
        params = {"openId" : self.openId}
        try:
            
            res = requests.post(url, json=data, headers=headers, params=params)

            match res.status_code:
                case 200:
                    print(200, "OK", res.content)
                    return json.loads(res.content)["id"]
                case 400:
                    print(400, "Invalid request")
                    return None
                case 401:
                    print(401, "Unauthorized")
                    return None
                case 413:
                    print(413, "File too large")
                    return None
                case 500:
                    print(500, "Internal server error")
                    return None
                case _:
                    print("Unknown error")
                    return None
                
        except Exception as e:
            print("create resource error:", e)
            return None

if __name__ == "__main__":
    pass
        