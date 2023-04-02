import requests
import json
import time

forker_name = "USERNAME1"  # fork到这个用户里
forker_pwd = "PASSWORD"  # personal access token
forkee_name = "USERNAME2"  # 需要被fork的用户
interval = 17  # 每个仓库fork的时间间隔，单位：秒
write2file = True  # 是否将被fork的用户所有仓库地址写到文件里

####################################################################
####################################################################
####################################################################

api_url_get = f"https://api.github.com/users/{forkee_name}/repos"
repositories = []
repository_urls = []
page_number = 1
while True:
    # 发送API请求并检查响应状态码
    response_get = requests.get(api_url_get, params={"per_page": 100, "page": page_number})
    if response_get.status_code != 200:
        print(f"Failed to get repositories for user {forkee_name}. Status code: {response_get.status_code}")
        break

    # 解析JSON响应并将仓库信息添加到repositories列表中
    repository_data = json.loads(response_get.content)
    if len(repository_data) == 0:
        break
    repositories += repository_data
    page_number += 1

if write2file:
    # 将仓库信息写入文件
    file_name = f"{forkee_name}_Github_Repos.txt"
    with open(file_name, "w") as file:
        # 遍历所有获取到的仓库
        for repository in repositories:
            file.write(f"{repository['html_url']}\n")
            repository_urls.append(repository['html_url'])
    print(f"All repositories of {forkee_name} are saved in file '{file_name}'.")

# 使用GitHub API将每个仓库fork到你的GitHub账户中，并同时star
for url in repository_urls:
    ### print(url)
    # 从URL中解析出owner和repo名称
    splitted_str_arr = url.split("/")
    owner = splitted_str_arr[len(splitted_str_arr) - 2]
    repo = splitted_str_arr[len(splitted_str_arr) - 1]
    print(f"Start forking {repo}...")

    ##################################################################
    # 发送API请求以fork仓库
    api_url_fork = f"https://api.github.com/repos/{owner}/{repo}/forks"
    response_fork = requests.post(api_url_fork, auth=(forker_name, forker_pwd))

    # 检查响应状态码和JSON响应中的信息
    if response_fork.status_code == 202:
        print(f"Successfully forked {url}.")
    else:
        error_message = json.loads(response_fork.content)["message"]
        print(f"Failed to fork {url}. Error message: {error_message}")
    time.sleep(interval)

    ##################################################################
    # 发送API请求以star仓库
    api_url_star = f"https://api.github.com/user/starred/{owner}/{repo}"
    response_star = requests.put(api_url_star, auth=(forker_name, forker_pwd))

    # 检查响应状态码和JSON响应中的信息
    if response_star.status_code == 204:
        print(f"Successfully starred {url}.")
    else:
        error_message = json.loads(response_star.content)["message"]
        print(f"Failed to star {url}. Error message: {error_message}")
    time.sleep(interval + 1)
