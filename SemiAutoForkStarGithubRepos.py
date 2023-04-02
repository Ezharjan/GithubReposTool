import requests
import json
import time

forker_name = "USERNAME"  # fork到这个用户里
forker_pwd = "PASSWORD"  # personal access token
urls_file = 'URLs.txt' # 存放用户仓库地址列表的外部文件名
interval = 10  # 每个仓库fork的时间间隔，单位：秒

####################################################################
####################################################################
####################################################################

repository_urls = []

# 将所有获取到的地址读进来（不要频繁获取用户仓库列表，否则会被限制IP）
with open(urls_file, 'r') as f:
    # 逐行读取文件中的 URL
    for line in f.readlines():
        # 处理读取到的 URL
        url = line.strip() # 去掉每一行的换行符

        # 在这里可以将 URL 传递给其他函数进行处理，例如进行 HTTP 请求等等
        print("Processing URL:", url)
        repository_urls.append(url)


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
