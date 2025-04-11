import requests
import web3
from web3 import Web3
import time
import json


class MonadTale(object):
    def __init__(self, address, proxies):
        self.address = address
        self.proxies = proxies

        # 定义连接时使用的请求头信息
        self.headers = {
                "authority": "mscore.onrender.com",
                "method": "post",
                "path": "/user",
                "scheme": "https",
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "content-length": "75",
                "content-type": "application/json",
                "origin": "https://monadscore.xyz",
                "pragma": "no-cache",
                "priority": "u=1, i",
                "referer": "https://monadscore.xyz/",
                "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            }

    def get_sign_msg(self, max_retries=3, retry_delay=5):
        """
        获取签名消息（带重试机制）

        参数：
        max_retries: 最大重试次数 (默认3次)
        retry_delay: 重试间隔秒数 (默认5秒)
        """
        # web3_t = Web3(Web3.HTTPProvider(self.rpc))
        url = f'https://mscore.onrender.com/user'
        data = {
                "wallet": self.address,
                "invite": "Y3G7JK1G"
        }
        print(data)
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(url, headers=self.headers, json=data, proxies=self.proxies)
                # 打印调试信息
                print(f"第{attempt+1}次尝试 | 状态码: {response.status_code}")
                print(f"响应内容: {response.text}...")  # 截断长内容

                # 检查HTTP状态码
                response.raise_for_status()
                # 成功响应处理
                if response.status_code == 200:
                    token = response.json()['token']
                    return token

                # 处理其他2xx状态码
                print(f"意外成功状态码: {response.status_code}")
                token = response.json()['token']
                return token

            except requests.exceptions.RequestException as e:
                # 网络请求类错误处理
                print(f"请求异常: {str(e)}")
                if attempt < max_retries:
                    print(f"{retry_delay}秒后重试...")
                    time.sleep(retry_delay)

            except Exception as e:
                print(f"其他错误: {str(e)}")
                return None

    def running(self):
        url = f'https://mscore.onrender.com/user/update-start-time'
        # 获取当前时间戳（毫秒级）
        token = self.get_sign_msg()
        current_timestamp = int(time.time() * 1000)
        data = {
                "wallet": self.address,
                "startTime": current_timestamp
            }
        # 添加Authorization头
        self.headers["Authorization"] = f"Bearer {token}"
        response = requests.put(url, headers=self.headers, json=data, proxies=proxies)
        print(response.json())

    def daily_tasks(self):
        task_id = ["task001", "task002", "task003"]
        url = f'https://mscore.onrender.com/user/claim-task'
        for task in task_id:
            data = {
              "wallet": self.address,
              "taskId": task
            }
            response = requests.post(url, headers=self.headers, json=data, proxies=proxies)
            print(response.json())


if __name__ == '__main__':
    rpc = "https://testnet-rpc.monad.xyz/"
    # web3_t = Web3(Web3.HTTPProvider(rpc))  # 使用 HTTPProvider 连接到以太坊主网
    proxies = ”替换为你的代理“
    web3_t = Web3(Web3.HTTPProvider(rpc))  # 使用 HTTPProvider 连接到以太坊主网
    with open("address.json", "r") as f:
        data = json.load(f)

    # 遍历所有钱包信息
    for entry in data:
        private_key = entry['private_key']  # 从 JSON 读取私钥
        account = web3.Account.from_key(private_key)
        address = account.address
        M = MonadTale(address, proxies)
        # M.get_sign_msg()
        M.running()
        # M.daily_tasks()

