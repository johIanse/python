import requests
import re
import os
from notify import send  # 青龙通知模块，如果不需要推送功能，可以注释或删除此行

# 设置代理（如果不需要代理，可以直接删除此部分）
proxies = {
    "http": "http://180.101.50.249:443",
    "https": "http://180.101.50.249:443",
}

# 基本 URL 和请求头
bbs_url = "https://bbs.binmt.cc/member.php"
credit_url = "https://bbs.binmt.cc/home.php?mod=spacecp&ac=credit"
credit_log_url = "https://bbs.binmt.cc/home.php"  # 积分收益记录页面
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'
}

credit_headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 14; zh-cn; 22127RK46C Build/UKQ1.230804.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.118 Mobile Safari/537.36 XiaoMi/MiuiBrowser/18.2.150419',
}


# 功能：获取登录页面中的 loginhash 和 formhash
def getLoginHashes(session):
    params = {
        'mod': 'logging',
        'action': 'login'
    }
    login_res = session.get(url=bbs_url, headers=headers, params=params, proxies=proxies)
    try:
        loginhash = re.search(r'loginhash=(.+?)"', login_res.text).group(1)
    except:
        print("获取 loginhash 失败，退出")
        return False
    try:
        formhash = re.search(r'name="formhash" value="(.+?)"', login_res.text).group(1)
    except:
        print("获取 formhash 失败，退出")
        return False
    return loginhash, formhash


# 功能：登录账号
def login(session, loginhash, formhash, username, password, loginfield="username"):
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
        'username': username,
        'password': password,
        'questionid': '0',
        'answer': ''
    }
    res = session.post(url=bbs_url, headers=headers, params=params, data=data, proxies=proxies)
    if '欢迎您回来' in res.text or "手机号登录成功" in res.text:
        return True
    else:
        print("登录失败\n", res.text)
        return False


# 功能：签到
def checkin(session):
    checkin_res = session.get(url='https://bbs.binmt.cc/k_misign-sign.html', headers=headers, proxies=proxies)
    try:
        checkin_formhash = re.search('name="formhash" value="(.+?)"', checkin_res.text).group(1)
    except:
        return "签到 formhash 查找失败，退出"
    res = session.get(
        f'https://bbs.binmt.cc/plugin.php?id=k_misign%3Asign&operation=qiandao&format=empty&formhash={checkin_formhash}',
        headers=headers,
        proxies=proxies
    )
    if "![CDATA[]]" in res.text:
        return '🎉 签到成功'
    elif "今日已签" in res.text:
        return '🐔 今日已签'
    else:
        print("签到失败\n", res.text)
        return '签到失败'


# 功能：格式化签到信息
def checkinfo(session):
    res = session.get(url='https://bbs.binmt.cc/k_misign-sign.html', headers=headers, proxies=proxies)
    try:
        user = re.search('class="author">(.+?)</a>', res.text).group(1)
        lxdays = re.search('id="lxdays" value="(.+?)"', res.text).group(1)
        lxlevel = re.search('id="lxlevel" value="(.+?)"', res.text).group(1)
        lxreward = re.search('id="lxreward" value="(.+?)"', res.text).group(1)
        lxtdays = re.search('id="lxtdays" value="(.+?)"', res.text).group(1)
        paiming = re.search('您的签到排名：(.+?)<', res.text).group(1)
        msg = (
            f"┌─【MT论坛账号】\n"
            f"├ 用户名：{user}\n"
            f"├ 连续签到：{lxdays} 天\n"
            f"├ 签到等级：Lv.{lxlevel}\n"
            f"├ 积分奖励：{lxreward}\n"
            f"├ 签到天数：{lxtdays} 天\n"
            f"└ 签到排名：{paiming}\n"
        )
    except Exception as e:
        msg = f"获取用户信息失败: {e}"
    return msg


# 功能：积分收益记录
def getCreditLogs(session):
    params = {
        'mod': 'spacecp',
        'ac': 'credit',
        'op': 'log',
        'km': '1'
    }
    res = session.get(url=credit_log_url, headers=credit_headers, params=params, proxies=proxies)
    try:
        pattern = re.compile(
            r'<div class="cre_mun.*?">金币.*?<span.*?>(.*?)</span>.*?</div>.*?<h2><span.*?>(.*?)</span>.*?<span.*?>(.*?)</span>',
            re.S
        )
        logs = pattern.findall(res.text)
        if logs:
            msg = "【积分收益记录】\n"
            msg += "┌─ 最新 5 条记录\n"
            for i, log in enumerate(logs[:5], 1):  # 提取最近 5 条记录
                amount = log[0]
                timestamp = log[1]
                description = log[2]
                msg += f"├ {i}. 时间：{timestamp}\n"
                msg += f"│    金币：{amount}\n"
                msg += f"│    原因：{description}\n"
            msg += "└───────────────\n"
        else:
            msg = "未找到积分收益记录\n"
    except Exception as e:
        msg = f"获取积分收益记录失败: {e}\n"
    return msg


# 功能：处理多个账户
def process_accounts(accounts_env):
    accounts = accounts_env.split('&')
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
                msg = f"【{username}】获取 loginhash 或 formhash 失败\n"
            else:
                if "@" in username:
                    loginfield = "email"
                else:
                    loginfield = "username"
                if login(session, hashes[0], hashes[1], username, password, loginfield) is False:
                    msg = f"【{username}】账号登录失败\n"
                else:
                    login_msg = f"【{username}】登录成功\n"
                    c = checkin(session)
                    info = checkinfo(session)
                    credits = getCreditLogs(session)
                    msg = f"{login_msg}\n{info}{c}{credits}"
            all_msgs.append(msg)
        except Exception as e:
            print(f"处理账号 {account} 时出错: {e}")
            all_msgs.append(f"处理账号 {account} 时出错: {e}")
    return all_msgs


# 主函数
if __name__ == "__main__":
    if 'MT_BBS' in os.environ:
        mt_bbs_value = os.environ['MT_BBS']  # 青龙面板中的环境变量，格式：username1;password1&username2;password2
        print("### MT论坛签到 ###")
        result = process_accounts(mt_bbs_value)
        if result:
            # 推送通知
            send('MT论坛签到', '\n————————————\n'.join(result))
        else:
            print('没有找到有效的账号信息，退出')
    else:
        print('未找到 MT_BBS 环境变量，退出')
