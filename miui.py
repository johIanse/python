#变量名   miui
#值       账号:密码&账号:密码

import requests
import os
import urllib3
from bs4 import BeautifulSoup

# 禁用 SSL 警告
urllib3.disable_warnings()

# 获取登录信息
credentials = os.environ.get('miui')
if credentials:
    for credential in credentials.split('&'):
        username, userpass = credential.split(':', 1)
        print('账号:', username)

        # 构造登录请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 14; zh-cn; 22127RK46C Build/UKQ1.230804.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.118 Mobile Safari/537.36 XiaoMi/MiuiBrowser/18.2.150419',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://miuiver.com',
            'referer': 'https://miuiver.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        data = {
            'log': username,
            'pwd': userpass,
            'action': 'mobantu_login',
        }

        # 发送登录请求
        response = requests.post('https://miuiver.com/wp-content/plugins/erphplogin//action/login.php', headers=headers, data=data, verify=False)

        if response.status_code == 200:
            # 获取登录后的 cookie 值
            cookies = response.cookies.get_dict()
            if any('wordpress_logged_in_' in key for key in cookies.keys()):
                print('登录成功')

                # 签到
                headers2 = {
                    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 14; zh-cn; 22127RK46C Build/UKQ1.230804.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.118 Mobile Safari/537.36 XiaoMi/MiuiBrowser/18.2.150419',
                    'x-requested-with': 'XMLHttpRequest',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://miuiver.com',
                    'referer': 'https://miuiver.com/user-profile/',
                    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cookie': '; '.join([f'{key}={value}' for key, value in cookies.items()])
                }

                data2 = {
                    'action': 'epd_checkin',
                }
                response2 = requests.post('https://miuiver.com/wp-admin/admin-ajax.php', headers=headers2, data=data2, verify=False)

                # 输出签到状态
                if response2.status_code == 200:
                    result = response2.json()
                    if result['status'] == 201:
                        print('已经签到过了')
                    elif result['status'] == 200:
                        print('已签到')
                    else:
                        print('签到失败:', result)
                else:
                    print('签到请求失败:', response2.text)

                # 获取个人中心页面
                response3 = requests.get('https://miuiver.com/user-profile/', headers=headers2, verify=False)

                if response3.status_code == 200:
                    # 解析HTML内容
                    soup = BeautifulSoup(response3.content, 'html.parser')
                    profile_boxes = soup.find_all('div', class_='profile-box')
                    
                    # 查找包含积分信息的profile-box
                    for box in profile_boxes:
                        if '积分明细' in box.text:
                            points_info = box.find_all('b')
                            if len(points_info) >= 2:
                                current_points = points_info[0].text
                                used_points = points_info[1].text

                                print(f'当前积分: {current_points}')
                                print(f'已用积分: {used_points}')
                            else:
                                print('未找到积分信息')
                            break
                    else:
                        print('未找到包含积分信息的 profile-box')
                else:
                    print('获取个人中心页面失败:', response3.text)
            else:
                print('登录失败，未找到登录cookie')
        else:
            print('登录请求失败:', response.text)
else:
    print('未找到登录信息')
