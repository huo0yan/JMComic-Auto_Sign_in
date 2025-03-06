import cv2
import json
import time
import socks
import socket
import requests
import pyautogui
import numpy as np
from DrissionPage import ChromiumPage, ChromiumOptions

#通过图片识别目标位置并点击
def find_and_click(template_path, threshold=0.1):

    # 截取当前屏幕
    screenshot = pyautogui.screenshot()

    # 将截图转换为OpenCV
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 加载cloud图片
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"错误：无法加载图片 {template_path}")
        return
    
    # 获取目标图片的高度和宽度
    template_height, template_width = template.shape[:2]

    # 使用模板匹配算法在屏幕截图中查找目标图片
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    
    # 获取匹配结果的最小值、最大值以及对应的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 检查匹配度是否超过阈值
    if max_val < threshold:
        print(f"未找到目标图片，最大匹配度：{max_val}")
        return

    # 计算目标图片的中心位置
    top_left = max_loc  # 目标图片的左上角位置
    center_x = top_left[0] + template_width // 2  # 中心点 X 坐标
    center_y = top_left[1] + template_height // 2  # 中心点 Y 坐标

    # 移动鼠标到目标位置并点击
    pyautogui.moveTo(center_x, center_y, duration=0.5)  # 移动到目标位置
    pyautogui.click()  # 点击
    print(f"已点击目标位置：({center_x}, {center_y})")

#打开浏览器网页
def open_browser_with_proxy(BASE_URL, proxy):

    # 创建浏览器配置对象
    co = ChromiumOptions()
    co.incognito()  # 启用隐身模式
    co.set_local_port(10086)  # 设置浏览器本地端口
    co.set_argument('--proxy-server', proxy)  # 设置代理
    co.set_argument(f'--user-agent', User_Agent)  # 设置UA
    co.set_browser_path(browser_path)

    # 启动浏览器
    browser = ChromiumPage(co)
    browser.clear_cache()  # 清除浏览器缓存
    browser.set.auto_handle_alert()  # 自动处理弹窗
    browser.set.window.max()  # 最大化浏览器窗口

    # 打开目标网页
    tab = browser.latest_tab  # 获取最新标签页
    tab.get(BASE_URL, timeout=30)  # 访问目标网页，设置超时时间为30秒
    print(f"已打开网页：{BASE_URL}")

    return browser  # 返回浏览器实例

#获取指定Cookie的值
def get_cookie_value(browser, cookie_name):
    # 获取所有 Cookie
    cookies = browser.cookies()
    # 遍历 Cookie 列表，查找指定名称的 Cookie
    for cookie in cookies:
        if cookie['name'] == cookie_name:
            return cookie['value']  # 返回 Cookie 的值
    return None  # 如果未找到，返回 None

#登录签到
def sign_in(cf_clearance):

    LOGIN_URL = f'{BASE_URL}/login'                      # 登录URL
    SIGN_URL = f'{BASE_URL}/ajax/user_daily_sign'        # 签到URL
    LOGOUT_URL = f'{BASE_URL}/logout'                    # 退出URL

    set_cookies = {
        'cf_clearance': cf_clearance
    }

    # 请求头
    headers = {
        'User-Agent': User_Agent,
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
                SIGN_response = session.post(SIGN_URL, headers=headers,  cookies=set_cookies)

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
                SIGN_response = session.post(SIGN_URL, headers=headers, cookies=set_cookies)
                # print(SIGN_response.text)
                if not "error" in json.loads(SIGN_response.text):
                    print("账号登出成功")
                else:
                    print("账号登出失败")
            else:
                print("登录失败:", response_data['errors'])
        else:
            if LOGIN_response.status_code == 403:
                print("Cloudflare验证")
                print(LOGIN_response.text)
            else:
                print("发送登录请求失败")

if __name__ == "__main__":

    # URL
    BASE_URL = "https://18comic.org"

    # 账号密码
    LOGIN_DATA = {
        'username': 'username',
        'password': 'password',
        'submit_login': '1',
    }
    
    # 是否需要设置socks代理
    set_proxy = True
    proxy_host = "127.0.0.1"
    proxy_port = 10808
    # 浏览器代理地址
    proxy = f"socks5://{proxy_host}:{proxy_port}"

    # 识别图片路径
    template_path = "cloud.jpg"

    # 谷歌浏览器路径
    browser_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

    # 设置浏览器和签到UA
    User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"

    # 启动浏览器并打开网站
    browser = open_browser_with_proxy(BASE_URL, proxy)

    # 等待页面加载完成
    time.sleep(10)

    # 查找并点击目标图片
    find_and_click(template_path)

    # 等待点击后的加载
    time.sleep(5)

    # 获取cf_clearance
    cf_clearance = get_cookie_value(browser, "cf_clearance")
    if cf_clearance:
        print(f"成功获取 cf_clearance: {cf_clearance}")
    else:
        print("未找到 cf_clearance Cookie")

    # 关闭浏览器
    browser.close()

    # 获取到则执行签到
    if cf_clearance:
        sign_in(cf_clearance)

while True:
    user_input = input('请输入exit退出: ')
    if user_input == 'exit':
        break
    else:
        print("输入错误，请输入'exit'退出")
