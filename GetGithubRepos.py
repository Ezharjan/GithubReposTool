import requests
import json


user_name = "USERNAME"
write2file = True

api_url = f"https://api.github.com/users/{user_name}/repos"

repositories = []

page_number = 1
while True:
    # 发送API请求并检查响应状态码
    response = requests.get(api_url, params={"per_page": 100, "page": page_number})
    if response.status_code != 200:
        print(f"Failed to get repositories for user {user_name}. Status code: {response.status_code}")
        break

    # 解析JSON响应并将仓库信息添加到repositories列表中
    repository_data = json.loads(response.content)
    if len(repository_data) == 0:
        break
    repositories += repository_data
    page_number += 1

if write2file:
    # 将仓库信息写入文件
    file_name = f"{user_name}_Github_Repos.txt"
    with open(file_name, "w") as file:
        # 遍历所有获取到的仓库
        for repository in repositories:
            file.write(f"{repository['html_url']}\n")
            print(f"{repository['html_url']}\n")

    print(f"All repositories of {user_name} are saved in file '{file_name}'.")
