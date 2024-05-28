'''
变量 MT_BBS 
值   账号;密码&账号;密码【英文的逗号;】
支持多个MT_BBS变量不一样的值
cron:  0 8 * * *
new Env('MT论坛签到
'''
import requests
import re
import os
from notify import send

proxies = {
    "http": "http://180.101.50.208:443",
    "https": "http://180.101.50.208:443",
}

bbs_url = "https://bbs.binmt.cc/member.php"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'}

def getLoginHashes(session):
    params = {
        'mod': 'logging',
        'action': 'login'
    }
    login_res = session.get(url=bbs_url, headers=headers, params=params, proxies=proxies)
    try:
        loginhash = re.search(r'loginhash=(.+?)"', login_res.text).group(1)
    except:
        print("登录loginhash查找失败，退出")
        return False
    try:
        formhash = re.search(r'name="formhash" value="(.+?)"', login_res.text).group(1)
    except:
        print("登录formhash查找失败，退出")
        return False
    return loginhash, formhash

def login(session, loginhash, formhash, u, p, loginfield="username"):
    params = {
        'mod': 'logging',
        'action': 'login',
        'loginsubmit': 'yes',
        'loginhash': loginhash,
        'inajax': '1'
    }
    data = {
        'formhash': formhash,
        'loginfield': loginfield,
        'username': u,
        'password': p,
        'questionid': '0',
        'answer': ''
    }
    res = session.post(url=bbs_url, headers=headers, params=params, data=data, proxies=proxies)
    if '欢迎您回来' in res.text:
        return True
    elif "手机号登录成功" in res.text:
        return True
    else:
        print("登录失败\n", res.text)
        return False

def checkin(session):
    checkin_res = session.get(url='https://bbs.binmt.cc/k_misign-sign.html', headers=headers, proxies=proxies)
    try:
        checkin_formhash = re.search('name="formhash" value="(.+?)"', checkin_res.text).group(1)
    except:
        return "签到formhash查找失败，退出"
    res = session.get(f'https://bbs.binmt.cc/plugin.php?id=k_misign%3Asign&operation=qiandao&format=empty&formhash={checkin_formhash}', headers=headers, proxies=proxies)
    if "![CDATA[]]" in res.text:
        return '🎉签到成功'
    elif "今日已签" in res.text:
        return '🐔今日已签'
    else:
        print(res.text)
        return '签到失败'

def checkinfo(session):
    res = session.get(url='https://bbs.binmt.cc/k_misign-sign.html', headers=headers, proxies=proxies)
    user = re.search('class="author">(.+?)</a>', res.text).group(1)
    lxdays = re.search('id="lxdays" value="(.+?)"', res.text).group(1)
    lxlevel = re.search('id="lxlevel" value="(.+?)"', res.text).group(1)
    lxreward = re.search('id="lxreward" value="(.+?)"', res.text).group(1)
    lxtdays = re.search('id="lxtdays" value="(.+?)"', res.text).group(1)
    paiming = re.search('您的签到排名：(.+?)<', res.text).group(1)
    msg = f'【MT论坛账号】{user}\n【连续签到】{lxdays}\n【签到等级】Lv.{lxlevel}\n【积分奖励】{lxreward}\n【签到天数】{lxtdays}\n【签到排名】{paiming}\n'
    return msg

if __name__ == "__main__":
    if 'MT_BBS' in os.environ:
        print("###MT论坛签到###")
        accounts = os.environ['MT_BBS'].split('&')
        all_msgs = []
        for account in accounts:
            if not account.strip():
                continue
            try:
                config = account.split(';')
                if len(config) != 2:
                    print(f"账号配置不完整: {account}")
                    continue
                username = config[0]
                password = config[1]
                session = requests.session()
                hashes = getLoginHashes(session)
                if hashes is False:
                    msg = f'【{username}】hash获取失败'
                else:
                    if "@" in username:
                        loginfield = "email"
                    else:
                        loginfield = "username"
                    if login(session, hashes[0], hashes[1], username, password, loginfield) is False:
                        msg = f'【{username}】账号登录失败'
                    else:
                        login_msg = f'{username}: 登录成功'
                        c = checkin(session)
                        info = checkinfo(session)
                        msg = f"{login_msg}\n{info}{c}"
                all_msgs.append(msg)
            except Exception as e:
                print(f"处理账号 {account} 时出错: {e}")
                all_msgs.append(f"处理账号 {account} 时出错: {e}")
        # 青龙通知推送
        send('MT论坛签到', '\n————————————\n'.join(all_msgs))
    else:
        print('未添加"MT_BBS"变量，退出')
