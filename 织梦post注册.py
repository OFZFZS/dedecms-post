#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import pytesseract
from PIL import Image
import re
import easye
import threading


class Mythread(threading.Thread):
    def run(self):
        # 每个线程循环注册50次
        for _ in range(50):
            userid = easye.getRandomChar(4, 2) + easye.getRandomNumber(3)
            pwd = easye.getRandomChar(2, 2) + easye.getRandomNumber(6)
            uname = userid
            email = easye.getRandomEmail()
            dedeRegister = DedeCMSRegister(userid, pwd, uname, email)
            dedeRegister.main()


class DedeCMSRegister:
    def __init__(self, userid, pwd, uname, email):
        self.vdcode = ""
        self.userid = userid
        self.pwd = pwd
        self.uname = uname
        self.email = email

    def register_check(self, content):
        # 这里返回的情况是动态写入的,因此不可以用lxml
        pattern = re.compile("document\.write\((.*?)\)")
        result = pattern.findall(content)[2]
        return result

    def register(self, ssion, url):
        data = {
            "userid": self.userid,
            "userpwd": self.pwd,
            "uname": self.uname,
            "userpwdok": self.pwd,
            "vdcode": self.vdcode,
            "dopost": "regbase",
            "email": self.email,
            "ste p": "1",
            "mtype": "个人",
            "safequestion": "0",
            "safeanswer": "",
            "sex": "",
            "agree": ""

        }
        response = ssion.post(url, data=data)
        loginResult = self.register_check(response.text)
        if loginResult.find("验证码") != -1:
            print("验证码错误!")
        else:
            print("注册可能成功了一次..")

    def getImgCode(self, filename):
        image = Image.open(filename)
        image.load()  # 加载一下图片，防止报错，此处可省略
        imgry = image.convert("L")  # 转换为灰度
        im_gary = imgry.point(lambda x: 0 if x < 143 else 255)  # 二值化处理
        vcode = pytesseract.image_to_string(image)
        self.vdcode = vcode.replace(" ", "")
        # print("验证码识别结果:", self.vdcode)

    def save_img(self, bytes):
        with open("vdimgck.php", "wb") as f:
            f.write(bytes)

    def getResponse(self, url, ssion):
        response = ssion.get(url)
        # response.content是bytes类型
        return response.content

    def requestPost(self, url, data, ssion):
        response = ssion.post(url, data=data)
        return response.content

    def checkState(self, session):
        "检查邮箱用户名等是否可用"
        data1 = {
            "dopost": "checkmail",
            "fmdo": "user",
            "email": self.email
        }
        check_mail = self.requestPost("http://localhost/member/index_do.php", data1, session)
        # print(check_mail.decode())

    def main(self):
        # ssion可以很方便的保存本次会话的cookie等信息
        ssion = requests.session()
        # 识别验证码,排除失败次数直到长度为四位为止,降低失败几率
        try:
            while len(self.vdcode) < 4:
                bytes_img = self.getResponse("http://localhost/include/vdimgck.php", ssion)
                # 上锁
                # myLock.acquire()
                self.save_img(bytes_img)
                self.getImgCode("vdimgck.php")
                # myLock.release()
            self.checkState(ssion)
            self.register(ssion, "http://localhost/member/reg_new.php")
        except Exception as error:
            print(error)


if __name__ == '__main__':
    # 看情况选择上不上锁
    # myLock = threading.Lock()
    # 开启5个线程
    for _ in range(5):
        mythread = Mythread()
        mythread.start()

    # 显示正在运行的线程
    # print(threading.enumerate())
