#!/usr/bin/env python
# -*- coding:utf-8 -*-
#作者: OFZFZS
import random


def getRandomIpHeader():
    """
    返回一个随机IP组成的协议头，伪装自己的IP
    """
    randomIpHeader = {}
    A = random.randint(0, 255)
    B = random.randint(0, 255)
    C = random.randint(0, 255)
    D = random.randint(0, 255)
    # str.join(序列) ".".join((str(A), str(B), str(C), str(D)))   str为分隔符, 序列里面如果有非字符串型貌似不可以
    # 组合为一个完整的IP
    random_ip = ".".join((str(A), str(B), str(C), str(D)))

    # 组合为字典，方便调用
    randomIpHeader["X-Forwarded-For"] = random_ip
    randomIpHeader["CLIENT_IP"] = random_ip
    randomIpHeader["VIA"] = random_ip
    randomIpHeader["REMOTE_ADDR"] = random_ip

    return randomIpHeader


def getUserAgent(opt=0):
    """默认取随机 可选参数opt 1为Google Chrome 2为Android 3为Internet Explorer 4为iOS """
    chromeUA = [
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360Chrome)",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36 LBBROWSER",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 BIDUBrowser/7.5 Safari/537.36",
    ]
    ieUA = [
        "Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)",
        "Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.2)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    ]
    androidUA = [
        "Mozilla/5.0 (Linux; U; Android 4.1.1; zh-cn;  MI2 Build/JRO03L) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 XiaoMi/MiuiBrowser/1.0",
        "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19",
        "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
    ]
    iosUA = [
        "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
        "Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3"
    ]
    if opt == 0:
        UA = random.choice(chromeUA + iosUA + androidUA + ieUA)
    elif opt == 1:
        UA = random.choice(chromeUA)
    elif opt == 2:
        UA = random.choice(androidUA)
    elif opt == 3:
        UA = random.choice(ieUA)
    elif opt == 4:
        UA = random.choice(iosUA)
    else:
        UA = "error.."
    return UA


def getRandomChar(count=1, format=0):
    """
    返回随机数量的大小写英文字符串
    :param format: 默认小写, 0为小写 1为大写 2为随机大小写
    :param count: 返回的数量
    """
    result = ""
    for i in range(count):
        if format == 0:
            num = random.randint(97, 122)
            result += chr(num)
        elif format == 2:
            tuple1 = (65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
                      75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
                      85, 86, 87, 88, 89, 90, 97, 98, 99, 100,
                      101, 102, 103, 104, 105, 106, 107, 108,
                      109, 110, 111, 112, 113, 114, 115, 116,
                      117, 118, 119, 120, 121, 122)
            num = random.choice(tuple1)
            result += chr(num)
        else:
            num = random.randint(65, 90)
            result += chr(num)

    return result


def getRandomNumber(count=1):
    """
    返回指定数量的随机数字字符串, 默认返回一个
    :param count: 数量
    """
    result = ""
    for _ in range(count):
        result += str(random.randint(0, 9))
    return result


def getRandomEmail():
    """获取一个随机邮箱"""
    prefix = ""
    suffix = ["@qq.com", "@126.com", "@139.com",
              "@gmail.com", "@sina.com.cn", "@163.com"]
    str1 = getRandomNumber(15) + getRandomChar(5, 2)
    for _ in range(random.randint(6, 10)):
        prefix += str1[random.randint(0, len(str1) - 1)]
    randomEmail = prefix + suffix[random.randint(0, len(suffix) - 1)]
    return randomEmail


if __name__ == '__main__':
    print(getRandomEmail())
