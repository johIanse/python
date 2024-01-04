import os
import requests
import json
import time


qmyybx_values = os.getenv('qmyybx')

if qmyybx_values is None:
    print("环境变量qmyybx未设置")
else:
    user_ids = qmyybx_values.split('#')

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3185 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/6210 MicroMessenger/8.0.16.2040(0x2800105F) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64] Edg/98.0.4758.102",
        "Cookie": ""  
    }

    for user_id in user_ids:
        headers['Cookie'] = f"user={user_id}"
        response = requests.get(f"https://www.magicalsearch.cc/api/store/getCoin?userId={user_id}", headers=headers)

        if response.status_code == 200:
            try:
                response_data = json.loads(response.text)
                print(f"Response data for user {user_id}: {response_data}") 
                coins = int(response_data['data'])
                print(f"Coins value for user {user_id}: {coins}")  
                print(f"Before condition: user {user_id} has {coins} coins")
                if coins == 0:
                    print(f"账号ID:{user_id} 今日已开宝箱")
                else:
                    print(f"账号ID:{user_id} 宝箱爆出了: {coins} 硬币")
                print(f"After condition: user {user_id} has {coins} coins")
            except json.JSONDecodeError:
                print("解析JSON失败")
            except ValueError:
                print("数据格式转换错误")
        else:
            print(f"请求失败，状态码：{response.status_code}")
        time.sleep(1)
