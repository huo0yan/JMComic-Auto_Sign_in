# JMComic 禁 漫 天 堂 自动签到
 
 第一次做，大佬勿喷勿喷

*整月签满，可额外获得涩图

期间忘记没签上，这个月就白签，所以才想自动签到的python脚本

## 使用方法：
只需要修改py文件内的账号密码即可，双击运行即可食用

自动登录、自动签到、自动退出 不放心可以看代码内容

## JMComic_Sign_in-Max.py:
通过打开浏览器识别图片模拟鼠标点击绕过Cloud并获取cf_clearance

需要自己设置的都在__main__里，默认谷歌浏览器

需把cloud.jpg下载同一个文件夹下才能识别

需要安装的依赖
  ```
pip install opencv-python PySocks requests pyautogui numpy DrissionPage pyscreeze pillow
  ```

## JMComic_Sign_in-proxy.py:
访问频繁封IP了，选用proxy了，可以选择关闭和开启，但需修改网址

403是Cloudflare验证，不会绕过只能手动填cf_clearance的值和浏览器UA对应

自己手动验证Cloud后再获取cf_clearance和UA的值才能访问

"而且有时效性，不能长期使用"

不知道该怎么绕过了，有大佬懂绕过的话可以自己修改代码
