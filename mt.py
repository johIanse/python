import requests
import json
import os

bl = os.environ.get('mt_ck')
if bl:
    mt_ck = 'JSESSIONID=' + bl
else:
    print('请设置环境变量 mt_ck')
    exit()
    
url1 = "https://api.mitangwl.cn/app/my/queryMyApprointmentList"
url2 = "https://api.mitangwl.cn/app/my/appointmentSign"

headers = {
    'Cookie': mt_ck
}

data = {}

response = requests.post(url=url1, headers=headers, json=data)

response_json = response.json()

user_list = response_json['data']['list'][0]['userList']
for user in user_list:
    nick_name = user['nickName']
    print(nick_name)

data2 = {"appointmentId": int(response_json['data']['list'][0]['appointmentId'])}

response2 = requests.post(url=url2, headers=headers, json=data2)

response_json = json.loads(response2.content)

msg = response_json.get('msg')
print(msg)