import requests
import json

LOGIN_URL = 'https://18comic-blackmyth.club/login'                      # 登录URL
SIGN_URL = 'https://18comic-blackmyth.club/ajax/user_daily_sign'        # 签到URL
LOGOUT_URL = 'https://18comic-blackmyth.club/logout'                    # 退出URL

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'
}

# 用户名和密码
payload = {
    'username': 'username',
    'password': 'password',
    'submit_login': '1',
}

# 发送登录请求
with requests.Session() as session:
    LOGIN_response = session.post(LOGIN_URL, data=payload, headers=headers)
    
    # 成功返回200，不成功返回301
    if LOGIN_response.status_code == 200:

        #获取返回的json判断是否登录成功
        response_data = json.loads(LOGIN_response.text)

        #成功 {"status":1,"errors":["https:\/\/18comic-blackmyth.club"]}
        #失败 {"status":2,"errors":["\u65e0\u6548\u7684\u7528\u6237\u540d\u548c\/\u6216\u5bc6\u7801!"]}
        if response_data["status"] == 1:
            print("账号登录成功\n")

            # 输出登录成功后的cookie
            cookies = session.cookies.get_dict()
            print("Cookies:")
            for key, value in cookies.items():
                print(f"{key}: {value}")
            print("")

            # 访问签到
            SIGN_response = session.post(SIGN_URL, headers=headers)

            # 返回签到内容
            SIGN_response_data = json.loads(SIGN_response.text)
            if "error" in SIGN_response_data:
                print("签到失败,你已经签到过了")
            else:  
                print("签到成功:", SIGN_response_data['msg'])
                print("自动签到执行完成！")                
            print()
            #返回 {"msg":""} 没有登录
            #返回 {"msg":"","error":"finished"} 已经签到过了
            #返回 {"msg":"\u60a8\u5df2\u7d93\u5b8c\u6210\u6bcf\u65e5\u7c3d\u5230\uff0c\u7372\u5f97 [ JCoin:20 ]  [ EXP:20 ] \n"} 签到成功

            # 退出账号
            LOGOUT_response = session.get(LOGOUT_URL, headers=headers)

            # 退出账号会发生重定向，查找重定向网页内容来判断是否退出成功,内容很多很卡
            # if "您现在已经登出!" in LOGOUT_response.text:
            #     print("账号登出成功!")
            # else:
            #     print("账号退出失败!")


            # 输出cookie判断是否退出
            # cookies = session.cookies.get_dict()
            # print("Cookies:")
            # for key, value in cookies.items():
            #     print(f"{key}: {value}")
            

            # 访问签到页面判断是否登出，返回 {"msg":""} 就是退出了
            SIGN_response = session.post(SIGN_URL, headers=headers)
            if not "error" in json.loads(SIGN_response.text):
                print("账号登出成功")
            else:
                print("账号登出失败")
        else:
            print("登录失败:", response_data['errors'])
    else:
        print("登录失败")


while True:
    user_input = input('请输入exit退出: ')
    if user_input == 'exit':
        break
    else:
        print("输入错误，请输入'exit'退出")
