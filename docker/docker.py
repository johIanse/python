import requests
import json
from datetime import datetime


#根据环境自行填写域名
#https://docker.mom  【已墙，开代理访问】
#https://idocker.link    【未墙，可直接访问】
#https://idocker.gay    【未墙，可直接访问】
base_url = "https://idocker.gay/api/v1"

# 登录
login_url = base_url + "/passport/auth/login"
login_headers = {
    "Host": "idocker.gay",
    "content-type": "application/x-www-form-urlencoded",
}
login_data = {
    "email": '账号',
    "password": '密码',
}
login_response = requests.post(login_url, headers=login_headers, data=login_data)

#登录响应内容为Json
response_json = login_response.json()

#获取响应auth_data值ck
auth_data = response_json['data']['auth_data']

#调用ck发送第二个请求
fetch_url = base_url + "/user/plan/fetch"
fetch_headers = {
    "Host": "idocker.gay",
    "authorization": auth_data,
}
fetch_response = requests.get(fetch_url, headers=fetch_headers)

#解析第二个请求的响应内容为Json
fetch_response_json = fetch_response.json()
#从响应中找到包含"免费白嫖"的项目的ID
plan_id = None
for item in fetch_response_json['data']:
    if '免费白嫖' in item['name']:
        plan_id = item['id']
        break
#前提是已经找到了相应的项目ID
if plan_id is not None:
    
    #code是由'rongseven@'和当前月份数字组成的字符串优惠劵码
    code = f"rongseven@{datetime.now().month}"
    
    #使用获取到的plan_id项目id和code优惠劵发送第三个请求
    check_url = base_url + "/user/coupon/check"
    check_data = {
        "code": code,
        "plan_id": plan_id,
    }
    check_response = requests.post(check_url, headers=fetch_headers, data=check_data)
    #解析第三个请求的响应内容为Json，并打印出来
    check_response_json = check_response.json()
    #如果响应中存在'message'键，打印其值并停止执行
    if 'message' in check_response_json:
        print(check_response_json['message'])
    else:
        #打印验证后的优惠劵名称和优惠劵码的值
        print("成功获取: ", check_response_json['data']['name'] + "：" + check_response_json['data']['code'])

        # 使用获取到的ck, 项目id和优惠劵发送第四个请求
        save_url = base_url + "/user/order/save"
        save_headers = {
            "authorization": auth_data,
            "content-type": "application/x-www-form-urlencoded",
            "Host": "idocker.gay",
        }
        save_data = {
            "period": "month_price",
            "plan_id": str(plan_id),
            "coupon_code": code,
        }
        save_response = requests.post(save_url, headers=save_headers, data=save_data)

        #解析第四个请求的响应内容为Json，并打印订单号出来
        save_response_json = save_response.json()
        print("订单号：", save_response_json['data'])

else:
    print("没有找到包含'免费白嫖'的项目")
