# coding=utf-8

# 识别字符序列变换算法，当前支持标准的MD5、SHA-1、Base64，及主流的URL编码、HTML编码

import re
import sys


# MD5判断函数
def checkMD5(inStr):
    MD5KeyStrs = '0123456789abcdefABCDEF'
    inStr = inStr.strip()  # 判断MD5的时候把输入两端的空格切掉
    if (len(inStr) != 16) and (len(inStr) != 32):
        return False
    else:
        for eachChar in inStr:
            if eachChar not in MD5KeyStrs:
                return False
        return True


# SHA1判断函数
def checkSHA1(inStr):
    SHA1KeyStrs = '0123456789abcdefABCDEF'
    inStr = inStr.strip()  # 判断SHA-1的时候把输入两端的空格切掉
    if len(inStr) != 40:
        return False
    else:
        for eachChar in inStr:
            if eachChar not in SHA1KeyStrs:
                return False
        return True


# Base64判断函数
def checkBase64(inStr):
    Base64KeyStrs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    inStr = inStr.strip()  # 判断Base64的时候把输入两端的空格切掉
    if len(inStr) % 4 != 0:
        return False
    else:
        for eachChar in inStr:
            if eachChar not in Base64KeyStrs:
                return False
        return True


# URL编码判断函数
def checkURLCode(inStr):
    reURLCode = '%[0-9a-fA-F][0-9a-fA-F]'  # 正则表达式
    reResultList = re.findall(reURLCode, inStr)
    if len(reResultList) == 0:
        return False
    else:
        return True


# HTML编码判断函数
def checkHTMLCode(inStr):
    htmlEncodeTuple = ('&lt;', '&gt;', '&amp;', '&#039;', '&quot;', '&nbsp;', '&#x27;', '&#x2F;')
    for each in htmlEncodeTuple:
        if each in inStr:
            return True
    return False


# 总的调度函数，负责调用各个算法的判断函数
def checkInput(inStr):
    if checkMD5(inStr):
        resStr = 'MD5'
        return resStr
    if checkSHA1(inStr):
        resStr = 'SHA-1'
        return resStr
    if checkBase64(inStr):
        resStr = 'Base64'
        return resStr
    if checkURLCode(inStr):  # 考虑到 URL编码 与 HTML编码可能会同时出现
        resStr = 'URLCode'
        if checkHTMLCode(inStr):
            resStr = 'URLCode + HTMLCode'
            return resStr
        else:
            return resStr
    if checkHTMLCode(inStr):
        resStr = 'HTMLCode'
        return resStr

    resStr = 'UnKnown'
    return resStr


# Python主程序

if __name__ == '__main__':

    sstr="GLDM9lMIBglnFv7YKftLBGTPBuZ18dsRxq7lLFRmwHN"
    if len(sstr) > 1:  # 接受命令行输入
        inputStr = str(sstr)
        resultStr = checkInput(inputStr)
        print(resultStr)