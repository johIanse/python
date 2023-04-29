#变量名   miui
#值       账号:密码

import requests
import os
import urllib3
import http.cookies
import re
​
# 禁用 SSL 警告
urllib3.disable_warnings()
​
# 获取登录信息
credentials = os.environ.get('miui')
if credentials:
  for credential in credentials.split('#'):
#    print('Processing credential:', credential)
    username, userpass = credential.split(':')
    print('账号:', username)
#    print('Password:', userpass)
    # 在这里使用 username 和 userpass 变量来执行其他操作
​
# 构造登录请求
headers = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'miuiver.com',
}
​
data = {
    'log': username,
    'pwd': userpass,
    'action': 'mobantu_login',
}
​
# 发送登录请求
response = requests.post('https://miuiver.com/wp-content/plugins/erphplogin//action/login.php', headers=headers, data=data, verify=False)
​
# 获取登录后的 cookie 值   
cookie_value = re.findall(r'wordpress_logged_in_\w+[^;]+', response.headers['Set-Cookie'])[0]
​
cookies = {'wordpress_logged_in': cookie_value}
​
#print(cookie_value)
​
#print(cookies)
# 签到
​
headers2 = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 
    'cookie': cookie_value ,
    'Host': 'miuiver.com',
}
​
data2 = {
    'action': 'epd_checkin',
}
response2 = requests.post('https://miuiver.com/wp-admin/admin-ajax.php', headers=headers2, data=data2, verify=False)
​
# 输出签到状态
if response2.status_code == 200:
    result = response2.json()
    if result['status'] == 201:
        print('已经签到过了')
    elif result['status'] == 200:
        print('已签到')
    else:
        print('签到失败')
else:
    print(response2.text)