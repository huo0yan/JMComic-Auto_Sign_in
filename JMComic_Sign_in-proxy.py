import json
import socks
import socket
import requests

#是否需要设置socks代 理
set_proxy = True
proxy_host = "127.0.0.1"
proxy_port = 10808

#JM官方域名:18comic.vip                  官网需要‘代 理’才能访问，稳定不会报错，这里默认修改18comic.vip
BASE_URL = 'https://18comic.vip'        #如果运行报错可能是换域名了或访问不了

# 用户名和密码
LOGIN_DATA = {
    'username': '0933127895',
    'password': 'pccu1123',
    'submit_login': '1',
}
SIGN_DATA = {
    'daily_id':'49',
    'oldStep':'5',
}

LOGIN_URL = f'{BASE_URL}/login'                      # 登录URL
SIGN_URL = f'{BASE_URL}/ajax/user_daily_sign'        # 签到URL
LOGOUT_URL = f'{BASE_URL}/logout'                    # 退出URL

set_cookies = {
    'cf_clearance': 'ncUip2Nt49AQWr_1xduRBZ5lKf6QebvvVFBUbOOv9Wk-1730814812-1.2.1.1-Va1mnjlLnDAa6PZEof6u8IuQXBcP1IET4s0lBYu58GRK6xK3wyAU9gs0xtcMelgy1Z8iD3_aQ5__Fj_cHnr7.pKCbD2ao050bbkcJeeDu6KxanhF1kMQEdAdy3aD2ZGJNDk9vN0liVYPLKJ6bNs19lZ2eC8QlSIDlkTvStxQRAQW0ld4cGOhm5bnAbQmOcfBjbV9i5KpFJbt7JEWFZjmAYf7hQgT0EyhYw7W0YwU7LbNSG.n1ylnVl_u_alS4kclWSq7pI3yMcLKrpeC1X0nZzXhePVBqYJ_8oCqxRQuqD.ZV7Qee2_SEBkxDvmXZuMhDoSVDmeNk72VnJo4u9ATlewD1HsP465bZYZz2wJnV7Tbg8X7Ixfv3iApFbP2ZlQHlfdi5nDj3VkHXzD8XS4qqS8j6wY9Pcl6pYdkFrOVvxE9D2tQPM3SaOuAFLU7Fp4t'
}
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

#设置socks
def set_socks_proxy(set_proxy, proxy_host, proxy_port):
    if set_proxy:
        socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
        socket.socket = socks.socksocket
set_socks_proxy(set_proxy, proxy_host, proxy_port)

# 发送登录请求
with requests.Session() as session:
    LOGIN_response = session.post(LOGIN_URL, data=LOGIN_DATA, headers=headers, cookies=set_cookies)
    # 输入状态码
    # print(LOGIN_response)
    
    # 成功返回200，不成功返回301
    if LOGIN_response.status_code == 200:

        #获取返回的json判断是否登录成功
        response_data = json.loads(LOGIN_response.text)

        #成功 {"status":1,"errors":["https:\/\/18comic.vip"]}
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
            SIGN_response = session.post(SIGN_URL, headers=headers, data=SIGN_DATA, cookies=set_cookies)

            # 返回签到内容
            # print(SIGN_response.text)
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
            LOGOUT_response = session.get(LOGOUT_URL, headers=headers, cookies=set_cookies)

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
            SIGN_response = session.post(SIGN_URL, headers=headers, data=SIGN_DATA, cookies=set_cookies)
            # print(SIGN_response.text)
            if not "error" in json.loads(SIGN_response.text):
                print("账号登出成功")
            else:
                print("账号登出失败")
        else:
            print("登录失败:", response_data['errors'])
    else:
        if LOGIN_response.status_code == 403:
            print("403 Cloudflare验证")
        else:
            print("发送登录请求失败")


while True:
    user_input = input('请输入exit退出: ')
    if user_input == 'exit':
        break
    else:
        print("输入错误，请输入'exit'退出")
