import requests
import json
import time

name = "USERNAME" # Github username
pwd = "PASSWORD" # personal access token

# 要star的仓库地址列表
repository_urls = [
    "https://github.com/Ezharjan/X-PostProcessing-Library",
    "https://github.com/Ezharjan/ZergNotes"
]


interval = 10 # unit: seconds

# 使用GitHub API将每个仓库star到你的GitHub账户中
for url in repository_urls:
    # 从URL中解析出owner和repo名称
    splitted_str_arr = url.split("/")
    owner = splitted_str_arr[len(splitted_str_arr) - 2]
    repo = splitted_str_arr[len(splitted_str_arr) - 1]
    print(f"Start starring {repo}...")

    # 发送API请求以star仓库
    api_url = f"https://api.github.com/user/starred/{owner}/{repo}"
    response = requests.put(api_url, auth=(name, pwd))

    # 检查响应状态码和JSON响应中的信息
    if response.status_code == 204:
        print(f"Successfully starred {url}.")
    else:
        error_message = json.loads(response.content)["message"]
        print(f"Failed to star {url}. Error message: {error_message}")
    time.sleep(interval)
