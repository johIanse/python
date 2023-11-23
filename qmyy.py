#变量 qmyy
#值 账号:密码#账号:密码

import os
import hashlib
import requests
import uuid
import socket
import struct
import random
import datetime
import time
import threading

def random_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def sign_in(email, password):
    password_md5 = hashlib.md5(password.encode()).hexdigest()
    login_url = "http://www.magicalapp.cn/user/login"
    login_data = {
        "password": password_md5,
        "ip": random_ip(),
        "device": str(uuid.uuid4()),
        "email": email,
    }
    response = requests.post(login_url, data=login_data)
    if response.status_code != 200:
        print(f"账号 {email} 登录失败")
        return
    set_cookie = response.headers.get('Set-Cookie')
    if set_cookie is None:
        print(f"账号 {email} 登录失败，未获取到token")
        return
    token_key_value = set_cookie.split(';')[0]
    token = token_key_value.split('=')[1] if '=' in token_key_value else None
    if not token:
        print(f"账号 {email} 登录失败，未正确解析token")
        return
    sign_url = "http://www.magicalapp.cn/user/api/signDays"
    sign_headers = {
        "Token": token,
        "Host": "www.magicalapp.cn",
    }
    response = requests.get(sign_url, headers=sign_headers)
    get_info_url = "http://www.magicalapp.cn/user/api/getSign?page=1"
    get_info_headers = {
        "Token": token,
        "Host": "www.magicalapp.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.9.3"
    }
    get_info_response = requests.get(get_info_url, headers=get_info_headers)
    if get_info_response.status_code == 200:
        print(f"账号 {email} 签到成功")
    else:
        print(f"账号 {email} 签到失败，状态码：{get_info_response.status_code}")

qmyy_all = os.getenv('qmyy')
accounts = qmyy_all.split('#')
threads = []
for account in accounts:
    email, password = account.split(':', 1)
    thread = threading.Thread(target=sign_in, args=(email, password))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()
