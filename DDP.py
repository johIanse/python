"""
pip3 install requests rich
变量：DDP
值：手机号#密码&手机号#密码

"""


import os
import requests
import json
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

# 初始化rich的Console对象
console = Console()

def parse_accounts(ddp_value):
    accounts = []
    for account_str in ddp_value.split("&"):
        if "#" in account_str:
            username, password = account_str.split("#", 1)
            accounts.append({"username": username, "password": password})
    return accounts

def login(username, password):
    login_url = "http://app.ddpai.com/login"
    login_payload = {
        'password': password,
        'pcode': "0x1002",
        'client': "app",
        'from': "2",
        'username': f"+86-{username}"  
    }
    login_headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 15; 22127RK46C Build/AQ3A.240912.001)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip"
    }

    login_response = requests.post(login_url, data=login_payload, headers=login_headers)
    if login_response.status_code == 200:
        return login_response.json()
    else:
        raise Exception(f"登录失败，状态码: {login_response.status_code}")

def signin(session_id):
    signin_url = "http://appgw.ddpai.com:18080/market/api/v1/usermgr/submitPointsTask"
    signin_payload = {
        "taskCode": "1"
    }
    signin_headers = {
        'Host': "appgw.ddpai.com:18080",
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 15; 22127RK46C Build/AQ3A.240912.001)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json",
        'Cookie': f"JSESSIONID={session_id}"
    }

    signin_response = requests.post(signin_url, data=json.dumps(signin_payload), headers=signin_headers)
    if signin_response.status_code == 200:
        return signin_response.json()
    else:
        raise Exception(f"签到失败，状态码: {signin_response.status_code}")

def process_account(account):
    try:
        username = account["username"]
        password = account["password"]

        # 显示当前处理账号
        console.print(Panel.fit(f"正在处理账号: [bold cyan]{username}[/]", title="账号信息", style="blue"))

        # 登录
        login_data = login(username, password)
        session_id = login_data['error_info']['session']
        console.print("登录成功")

        # 签到
        signin_response = signin(session_id)
        if signin_response['error_code'] == 0:
            points = signin_response['error_info']['points']
            console.print(f"签到成功！当前积分: [bold yellow]{points}[/]")
        elif signin_response['error_code'] == 1064961:
            console.print("今天已经签到过了，无需重复签到。", style="bold yellow")
        else:
            console.print(f"签到失败，未知错误: {signin_response}", style="bold red")
    except Exception as e:
        error_text = Text(f"处理账号 {username} 时出错: {str(e)}", style="bold red")
        console.print(error_text)

# 主程序
def main():
    # 从环境变量中读取DDP变量
    ddp_value = os.getenv("DDP")
    if not ddp_value:
        console.print("请确保环境变量DDP已正确设置。", style="bold red")
        return

    # 解析账号信息
    accounts = parse_accounts(ddp_value)
    if not accounts:
        console.print("未解析到有效的账号信息。", style="bold red")
        return

    # 显示总账号数
    console.print(Panel.fit(f"共解析到 [bold green]{len(accounts)}[/] 个账号", title="账号统计", style="blue"))

    # 使用rich的Progress显示进度
    with Progress() as progress:
        task = progress.add_task("[cyan]处理账号中...", total=len(accounts))
        for account in accounts:
            process_account(account)
            progress.update(task, advance=1)
            console.print("-" * 40)  # 分隔线

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_text = Text(f"程序出错: {str(e)}", style="bold red")
        console.print(error_text)
