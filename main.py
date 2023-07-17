# -*- coding: utf-8 -*-
import json
import os
import sys
from memos import memos

from bs4 import BeautifulSoup



def html_memo_to_json(html):

    soup = BeautifulSoup(html, 'html.parser')
    export_json = []

    for item in soup.find_all(class_="memo"):

        content = ""
        files = []
        selected = item.select(".content p, .content li")

        for i, e in enumerate(selected):
            text = e.get_text()

            if i < len(selected) - 1:
                text += "\n"

            content += text

        for e in item.select("img"):
            src = e.get("src")
            files.append(src)
        export_json.append({
            "content": content,
            "filePath": files if files else None
        })
    return export_json


def main(argv):

    file_path = argv[0]
    openapi_url = argv[1]
    openId = argv[2]

    memos_json = []

    if file_path.endswith(".html"):
        with open(file_path, "r", encoding='utf-8') as f:
            html = f.read()

            memos_json += html_memo_to_json(html)

            print(f"finish: {len(memos_json)} data is exported")


    print("=====================================")
    print("start to import data to memos")
    
    memos_api = memos.Memos_api(openId, openapi_url)

    for i, item in enumerate(memos_json):

        memo = memos.Memos(content=item["content"], filePath=item["filePath"])

        memos_api.create_memo(memo)

        print("finish:", i + 1, "/", len(memos_json))

    print("finish: all data is imported")

if __name__ == "__main__":

    main(sys.argv[1:])

    


