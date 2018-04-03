#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import pytesseract
from PIL import Image
import re


class DedeCMSLogin:
    def __init__(self, userid, pwd):
        self.vdcode = ""
        self.userid = userid
        self.pwd = pwd

    def login_check(self, content):
        # 这里返回的情况是动态写入的,因此不可以用lxml
        pattern = re.compile("document\.write\((.*?)\)")
        result = pattern.findall(content)[2]
        return result

    def login(self, ssion, url):
        data = {
            "userid": self.userid,
            "pwd": self.pwd,
            "fmdo": "login",
            "dopost": "login",
            "keeptime": "604800",
            "vdcode": self.vdcode
        }
        response = ssion.post(url, data=data)
        loginResult = self.login_check(response.text)
        print(loginResult)

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

    def main(self):
        # ssion可以很方便的保存本次会话的cookie等信息
        ssion = requests.session()
        # 识别验证码,排除失败次数直到长度为四位为止,降低失败几率
        try:
            while len(self.vdcode) < 4:
                bytes_img = self.getResponse("http://localhost/include/vdimgck.php", ssion)
                self.save_img(bytes_img)
                self.getImgCode("vdimgck.php")
            self.login(ssion, "http://localhost/member/index_do.php")
        except Exception as error:
            print(error)



if __name__ == '__main__':
    for _ in range(10):
        dedeLogin = DedeCMSLogin("test001", "test123456")
        dedeLogin.main()
