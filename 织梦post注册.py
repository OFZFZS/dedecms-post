#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import pytesseract
from PIL import Image
import re
import multiprocessing
import os
import easye


class DedeCMSRegister():
    def __init__(self, userid, pwd, uname, email, q):
        self.vdcode = ""
        self.userid = userid
        self.pwd = pwd
        self.uname = uname
        self.email = email
        self.q = q  # 进程间通信

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
            self.q.put("验证码错误!")
        else:
            regResult = "用户名:%s|密码%s" % (self.uname, self.pwd)
            self.q.put(regResult)
            print("注册成功!用户名:%s  密码%s " % (self.uname, self.pwd))

    def getImgCode(self, filename):
        image = Image.open(filename)
        # image.load()  # 加载一下图片，防止报错，此处可省略
        # imgry = image.convert("L")  # 转换为灰度
        # im_gary = imgry.point(lambda x: 0 if x < 143 else 255)  # 二值化处理

        vcode = pytesseract.image_to_string(image)

        # 过滤掉识别出来多出来的空格
        self.vdcode = vcode.replace(" ", "")
        # print("验证码识别结果:", self.vdcode)

    def save_img(self, bytes):
        # 保存验证码到本地
        with open(str(os.getpid()) + ".php", "wb") as f:
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

    def doWork(self):
        # ssion可以很方便的保存本次会话的cookie等信息
        ssion = requests.session()
        # 识别验证码,排除失败次数直到长度为四位为止,降低失败几率
        try:
            while len(self.vdcode) < 4:
                bytes_img = self.getResponse("http://localhost/include/vdimgck.php", ssion)
                # 上锁
                # myLock.acquire()
                self.save_img(bytes_img)
                self.getImgCode(str(os.getpid()) + ".php")
                # myLock.release()
            self.checkState(ssion)
            self.register(ssion, "http://localhost/member/reg_new.php")
        except Exception as error:
            self.q.put("网络错误,请检查.")


def main(q):
    userid = easye.getRandomChar(4, 2) + easye.getRandomNumber(3)
    pwd = easye.getRandomChar(2, 2) + easye.getRandomNumber(6)
    uname = userid
    email = easye.getRandomEmail()
    dedeRegister = DedeCMSRegister(userid, pwd, uname, email, q)
    dedeRegister.doWork()


if __name__ == '__main__':
    # 建立进程池
    pool = multiprocessing.Pool(5)

    # 进程间通信
    q = multiprocessing.Manager().Queue()

    # 5个进程,总共注册250次
    for _ in range(250):
        pool.apply_async(func=main, args=(q,))

    # 接收进程执行结果
    for _ in range(250):
        result = q.get()
        print("result:", result)
        if result.find("验证码") == -1:
            # 保存登陆成功的用户名密码到本地
            with open("user.txt", "a", encoding="utf-8") as f:
                f.write(result + "\n")

    # 删除保存在本地的验证码文件
    fileList = os.listdir()

    for file in fileList:
        # 字符串切割,找到后缀为PHP的文件,遍历删除
        if file[-3:] == "php":
            os.remove(file)

    pool.close()
    pool.join()
