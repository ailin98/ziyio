'''
项目名：非梵艺术（数字产品）
当前版本：3.0
自用频道：https://t.me/StarOneDream
项目连接：https://static.feifan.art/app_static/feifanlogin.html?uid=1458649
一个长期项目，开局送一个白蛋，签到20天送两个宠物，还有碎片再换一个宠物，两个宠物换一个白蛋，白蛋孵出三个宠物，宠物一个利润十几块
变量 ff_token，格式：账号-密码（列如：123-321） 多账户\n隔开
当前就一个签到功能，自测会不会黑号，以后再加功能
'''

import requests
import time
import random
import os


ff_token = os.getenv('ff_token')
token_list = ff_token.split('\n')



user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]

def sign(token,feed_type):
    try:
        requests.KeepAlive = False
        now = str(time.time()).replace(".", "")[:10]
        url = f"http://feifanapi.feifan.art/app/egg/feed"
        headers = {
            "Host": "feifanapi.feifan.art",
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json;charset=UTF-8",
            "platform": "1",
            "token": token,
            "Content-Length": "17"
        }
        data = {
            "elementType": f'{feed_type}'
        }
        response = requests.post(url=url,headers=headers,json=data,timeout=5).json()

        print(response)
    except Exception as e:
        print(f"签到失败,可能今日已签到{e}")

def suipian(token):
    url = "http://feifanapi.feifan.art/app/egg/fragment"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Content-Type": "application/json;charset=UTF-8",
        "platform": "1",
        "token": token,
    }

    response = requests.get(url, headers=headers).json()

    return response['data']['fragment_count']

def pet(token):
    url = "http://feifanapi.feifan.art/app/egg/exchangePreview?elementType=1"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Content-Type": "application/json;charset=UTF-8",
        "platform": "1",
        "token": token,
    }

    response = requests.get(url, headers=headers).json()
    print(f'总数：{response["data"]["already_pet_count"]}只')
    print(f'离火：{response["data"]["alreadyHoldFirePetCount"]}只，坤土：{response["data"]["alreadyHoldSoilPetCount"]}只')


def get_my_info(token):
    url = "http://feifanapi.feifan.art/app/user/byToken"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Content-Type": "application/json;charset=UTF-8",
        "platform": "1",
        "token": token,
    }

    response = requests.get(url, headers=headers)



    if response.status_code==200:
        info=response.json()
        # print(info)
        name=info['data']['nickname']
        mobile=info['data']['mobile']
        register_time=info['data']['register_time']
        egg_level=info['data']['egg_level']
        suipians=suipian(token)
        print(f"""昵称：{name}
手机号：{mobile}
注册时间：{register_time}
坤蛋等级：LV {egg_level} 
当前碎片：{suipians} / 300""")
    else:
        print(f'当前账号读取信息失败')


def sign_days(token):
    url = "http://feifanapi.feifan.art/app/activity/sign/state"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Content-Type": "application/json;charset=UTF-8",
        "platform": "1",
        "token": token,
    }

    response = requests.get(url, headers=headers).json()

    print(f'共签到 {len(response["data"]["signedDays"])} 天')

def login(phone,passw):
    try:
        url = "https://feifanapi.feifan.art/app/user/login/byPassword"
        headers = {
            "Host": "feifanapi.feifan.art",
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json;charset=UTF-8",
            "platform": "1",
            "Content-Length": "52",
        }

        payload = {
            "mobile": phone,
            "password": passw,
        }

        response = requests.post(url, headers=headers, json=payload).json()
        print(f"登陆成功：{response['data']}")
        token=response['data']['token']
        return token
    except Exception as e:
        print(f'账号或密码错误{e}')


print(f'=======当前有{len(token_list)}个账号，开始运行========')
for index, token in enumerate(token_list):
    print(f'===============账号{index + 1}===============')
    phone_list=token.split('-')
    tokens=login(phone_list[0],phone_list[1])
    try:
        get_my_info(tokens)
        sign_days(tokens)
        pet(tokens)
        print('开始签到')
        for i in range(1,3):
            print(f'类型：{i} 正在进行投喂')
            sign(tokens,i)
    except:
        print(f'token过期或者出现其它错误')

