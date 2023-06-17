import requests
import json
import os
from time import sleep

mt_ck = os.environ.get('mt_ck')

if mt_ck:
    mt_ck_list = mt_ck.split('#')
    
    for mt_ck_str in mt_ck_list:
        mt_ck_values = mt_ck_str.split('&')
        ck = mt_ck_values[0].split('=')[1]
        zfb = mt_ck_values[1] if len(mt_ck_values) > 1 else ''
        xm = mt_ck_values[2] if len(mt_ck_values) > 2 else ''

#        print(xm, zfb, ck)


        url1 = "https://api.mitangwl.cn/app/my/queryMyApprointmentList"
        url2 = "https://api.mitangwl.cn/app/my/appointmentSign"
        url3 = "https://api.mitangwl.cn/app/my/queryUserBalance"
        url4 = "https://api.mitangwl.cn/app/my/applyCashOut"


        headers = {
           'Cookie': 'JSESSIONID=' + ck
        }

#        print(headers)
        data = {}

        response = requests.post(url=url1, headers=headers, json=data)

        response_json = response.json()

        for appointment in response_json['data']['list']:
            user_list = appointment['userList']
            for user in user_list:
                nick_name = user['nickName']
                print("拼团用户 : " + nick_name)

            data2 = {"appointmentId": int(appointment['appointmentId'])}

            sleep(120)
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


        sleep(120)
        response4 = requests.post(url4, json=payload, headers=headers)
        if response.status_code == 200:
           print(response4.json()['msg'])
        else:
           print("请求失败，状态码为：" + str(response.status_code))
else:
    print('请设置环境变量 mt_ck')
    exit()
    
    
