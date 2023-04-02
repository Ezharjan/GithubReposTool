import requests
import json
import time

name = "USERNAME" # Github username
pwd = "PASSWORD" # personal access token

# 要fork的仓库地址列表
repository_urls = [
    "https://github.com/Ezharjan/X-PostProcessing-Library",
    "https://github.com/Ezharjan/ZergNotes"
]


interval = 5 # unit: seconds

# 使用GitHub API将每个仓库fork到你的GitHub账户中
for url in repository_urls:
    # 从URL中解析出owner和repo名称
    splitted_str_arr = url.split("/")
    owner = splitted_str_arr[len(splitted_str_arr) - 2]
    repo = splitted_str_arr[len(splitted_str_arr) - 1]
    print(f"Start forking {repo}...")

    # 发送API请求以fork仓库
    api_url = f"https://api.github.com/repos/{owner}/{repo}/forks"
    response = requests.post(api_url, auth=(name, pwd))

    # 检查响应状态码和JSON响应中的信息
    if response.status_code == 202:
        print(f"Successfully forked {url}.")
    else:
        error_message = json.loads(response.content)["message"]
        print(f"Failed to fork {url}. Error message: {error_message}")
    time.sleep(interval)
