import requests
import time
import json
import threading

# 可填写多个ck
cks = ['ck1','ck2','ck3','ck4']

def afternoon_12(ck):
    couponReferId = '4D823738DC09463DAA54156094768F02'

    headers = {
        'Connection': 'keep-alive',
        'Content-Length': '2508',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://market.waimai.meituan.com',
        'mtgsig': '{"a1":"1.0","a2":1682748089966,"a3":"3u8vv9v619z35857zw022u7vx88773zx812x05yz83x97958x9644xu4","a4":"21bb3f8f8d1975ec8f3fbb21ec75198de11921ea0d6c3867","a5":"7W/X6lup/pCSVl3rdeQe4eD+GwnSpxk/maVbu04UXiJ7rkuOnBH5mkJmDQyZ6h/FcCG3RoaFmBUD5tolu3jWacAY5XZ=","a6":"h1.2dkmvQGh9ovBV5zkRbQ++7pV+OvXyTy8HvuUlI1R19xcO0PFPrLZTn6vT9YedCmpYvbOfkCv0G7fJ8bKHygbYaqxjQzSbAgJUmWlBcZ8QDkM5tzy3JqX0wZzRBgKVH62lBzzMIplbugBRb6HVKS4PdsAVscGFoIkZ9GClthcMomrJwS6cF+4/hbIHtWzw/5KenLiqWStTmjv8dtba6sbgIwFqMqprizBfJdSITIH2ArOzUfT3hF+rXJNDXO8oXR6+p0BDBrzPFaaFPskLWB2+DN5soMCxOwe39jFLqJsTir5Sesow4PnGkcUQVgZGIxGBS8N0rvsFCY0xVamkOm/Eo0y/lQG31Dyv4Kk1GZkEyeA15dEGaC4Ajj6+ADJewDbixuN9MYg/OliI1JFnrQuKHthLyOInSgiBzW2kgWhEDOaiu45FFV9Ky6mIlitfQWkGSIwoOIuawww55IjsD74jEw==","a7":"","x0":4,"d1":"208d492de9eedac3d5a8772993ca58cb"}',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 BingWeb/6.9.6',
        'Content-Type': 'application/json',
        'Referer': 'https://market.waimai.meituan.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': ck,
        'X-Requested-With': 'mark.via',
    }
    
    params = {
        'couponReferId': couponReferId,
        'actualLng': '121.84431',
        'actualLat': '29.89889',
        'geoType': '2',
        'gdPageId': '485507',
        'pageId': '487014',
        'version': '1',
        'utmSource': 'wxshare',
        'utmCampaign': '',
        'instanceId': '16825000747950.2133716842128197',
        'componentId': '16825000747950.2133716842128197',
    }

    json_data = {
        'cType': 'mti',
        'fpPlatform': 3,
        'wxOpenId': '',
        'appVersion': '',
        'mtFingerprint': 'H5dfp_1.8.2_tttt_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',
    }


    while True:
        response = requests.post(
            'https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/fetchcoupon',
            params=params,
            headers=headers,
            json=json_data,
        )
        if response.status_code == 200:
          try:
            json_data = response.json()
            if isinstance(json_data, dict) and 'msg' in json_data: 
              print(f'奶茶神卷: {json_data["msg"]}')
            elif isinstance(json_data, str):
              print(f'msg: {json_data}')
            else:
              print('未找到msg参数')
          except json.JSONDecodeError as e:
            print(f'解析JSON数据时发生错误: {str(e)}')
        else:
          print(f'请求失败，响应状态码为{response.status_code}')
          # 设置等待时间后再次发送请求
        time.sleep(0.002)

def main():
    threads = []
    for ck in cks:
        t = threading.Thread(target=afternoon_12, args=(ck,))
        threads.append(t)
        t.start()

if __name__ == '__main__':
    main()
