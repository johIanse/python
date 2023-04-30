import requests
import json
import os

mt_ck = os.environ.get('mt_ck')

if mt_ck:
    mt_ck_list = mt_ck.split('&')
    zfb = mt_ck_list[1].replace("'", "")
    xm = mt_ck_list[2].replace("'", "")
    ck = mt_ck_list[0]
else:
    print('请设置环境变量 mt_ck')
    exit()
    
print(xm,zfb,ck)

url1 = "https://api.mitangwl.cn/app/my/queryMyApprointmentList"
url2 = "https://api.mitangwl.cn/app/my/appointmentSign"
url3 = "https://api.mitangwl.cn/app/my/queryUserBalance"
url4 = "https://api.mitangwl.cn/app/my/applyCashOut"


headers = {
    'Cookie': ck
}

print(headers)
data = {}

response = requests.post(url=url1, headers=headers, json=data)

response_json = response.json()

for appointment in response_json['data']['list']:
    user_list = appointment['userList']
    for user in user_list:
        nick_name = user['nickName']
        print("拼团用户 : " + nick_name)

    data2 = {"appointmentId": int(appointment['appointmentId'])}

    response2 = requests.post(url=url2, headers=headers, json=data2)

    response_json = json.loads(response2.content)

    msg = response_json.get('msg')
    print(msg)

response3 = requests.post(url3, headers=headers)
content_str = response3.content.decode('utf-8')
content_json = response3.json()
amount = content_json['data']['amount']
print("账户余额 " + str(amount))


payload = {
    'alipayAccount': zfb,
    'alipayName': xm,
}


response4 = requests.post(url4, json=payload, headers=headers)
if response.status_code == 200:
    print(response4.json()['msg'])
else:
    print("请求失败，状态码为：" + str(response.status_code))
