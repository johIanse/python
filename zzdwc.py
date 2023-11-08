#变量zzdwc
#ck填写PlaceID#WechatId#PublicOpenID#CustID#cookie

import os
import json
import requests

params = os.getenv('zzdwc')
if params is None:
    print("环境变量zzdwc未设置")
else:
    params = params.split('#')
    if len(params) != 5:
        print("环境变量zzdwc格式错误")
    else:
        CustID = params[3]
        PublicOpenID = params[2]
        WechatId = params[1]
        PlaceID = params[0]
        cookie = params[4] 
        url1 = "http://pay.zk2016.com/api/web/getwealth.do"
        headers1 = {"Host": "pay.zk2016.com", "Content-Length": "138"}
        data1 = {"PlaceID": PlaceID, "WechatId": WechatId, "PublicOpenID": PublicOpenID}
        response1 = requests.post(url1, headers=headers1, data=json.dumps(data1))
        response_data1 = response1.json()
        username = response_data1.get('userinfo', {}).get('SecondName')
        print('用户名:', username)
        wealthlist = response_data1.get('wealthlist', [])
        wealth_before_sign = ''
        for item in wealthlist:
            if item.get('name') == '存币':
                wealth_before_sign = item.get('num')
        print('当前存币:', wealth_before_sign)
        url2 = "http://pay.zk2016.com/web/signin.do?PlaceID=" + PlaceID
        headers2 = {
            "Host": "pay.zk2016.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J17C Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5317 MMWEBSDK/20230805 MMWEBID/3914 MicroMessenger/8.0.42.2460(0x28002A35) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "X-Requested-With": "com.tencent.mm",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": cookie
        }
        response2 = requests.get(url2, headers=headers2)
        url3 = "http://pay.zk2016.com/api/web/SignIn.do"
        headers3 = {"Host": "pay.zk2016.com", "Content-Length": "98"}
        data3 = {"CustID": CustID, "PlaceID": PlaceID}
        response3 = requests.post(url3, headers=headers3, data=json.dumps(data3))
        result_msg = response3.json().get('ResultMsg')
        print('签到信息:', result_msg)
        response1 = requests.post(url1, headers=headers1, data=json.dumps(data1))
        response_data1 = response1.json()
        wealthlist = response_data1.get('wealthlist', [])
        wealth_after_sign = ''
        for item in wealthlist:
            if item.get('name') == '存币':
                wealth_after_sign = item.get('num')
        print('总存币:', wealth_after_sign)
        push_url = "https://www.pushplus.plus/send"
        PUSH_PLUS_TOKEN = os.getenv('PUSH_PLUS_TOKEN')
        if PUSH_PLUS_TOKEN is None:
            print("环境变量PUSH_PLUS_TOKEN未设置")
        else:
            push_data = {
                "token": PUSH_PLUS_TOKEN,
                "title": "郑州二七区城市英雄电玩城",
                "content": "用户名: {}\n当前存币: {}\n签到信息: {}\n总存币: {}".format(username, wealth_before_sign, result_msg, wealth_after_sign)
            }
            response = requests.post(push_url, data=push_data)
            if response.status_code != 200:
                print("Push+推送失败")
            else:
                print("Push+推送成功")
