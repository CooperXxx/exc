import urllib.request
import urllib.parse
import ssl
import http.cookiejar
import urllib
import schedule
import time
import pytesseract
from PIL import Image
from multiprocessing import Pool

from selenium import webdriver
import datetime
import random
import os
from multiprocessing import Process
from selenium.webdriver.support import expected_conditions as EC

def addmates(matesid,framenum,bro):

    button_addmates = bro.find_element_by_id("handle-add")
    button_addmates.click()
    bro.switch_to.frame("xubox_iframe"+str(framenum))
    input_matesid = bro.find_element_by_id("cardNo")
    input_matesid.send_keys(matesid)
    button_findmate = bro.find_element_by_class_name("search-id")
    button_findmate.click()
    input_existmates = bro.find_elements_by_class_name("user")
    oldcontacts = []
    for input_existmate in input_existmates:
        # print(input_existmate.get_attribute("textContent"))
        oldcontacts.append(input_existmate.get_attribute("textContent").strip())

    time.sleep(1)
    # print(bro.page_source)
    input_newcontact = bro.find_element_by_id("contact")
    # print(input_newcontact.get_attribute("textContent"))
    newcontact = input_newcontact.get_attribute("textContent")

    if newcontact not in oldcontacts:
        button_addtocontacts = bro.find_element_by_class_name("add-user")
        button_addtocontacts.click()
        time.sleep(1)
    else:
        for input_existmate in input_existmates:
            if input_existmate.get_attribute("textContent").strip() == newcontact:
                checkbox = input_existmate.find_element_by_name("user")
                checkbox.click()
                time.sleep(1)
                button_submitaddmates = bro.find_element_by_class_name("del-all-users")
                button_submitaddmates.click()
                break


def main(reserverdic):

    #隐藏浏览器界面
    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    # bro = webdriver.Chrome(chrome_options=option)
    bro = webdriver.Chrome()
    print("Chrome 已启动")
    url = 'https://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal'


    bro.get(url)
    # print(bro.page_source)

    # 登录预约系统
    id=reserverdic["idpwd"]["ssid"]
    pwd=reserverdic["idpwd"]["pwd"]
    input_username = bro.find_element_by_id("username")
    input_password = bro.find_element_by_id("password")
    input_username.send_keys(id)
    input_password.send_keys(pwd)
    # print(input_username)
    # print(input_password)

    # 多个class 要用下面的形式 不能直接find_element_by_class
    botton_login = bro.find_element_by_css_selector("[class='auth_login_btn primary full_width']")
    botton_login.click()

    # url3="http://yuyue.seu.edu.cn/eduplus/order/initOrderIndex.do?sclId=1"
    # bro.get(url3)
    #打开预约界面
    info = reserverdic["info"]
    # info = {
    #     'dayInfo': "2018-11-23",
    #     'itemId': 7,
    #     'time': "12:00-13:00"
    # }
    # infourl = urllib.parse.urlencode(info)
    """
        'itemId':7, 九龙湖乒乓,1-3人
        'itemId':8, 九龙湖篮球,全场9-14，半场5-8人
        'itemId':9, 九龙湖排球,4-15人
        'itemId':10, 九龙湖羽毛球,1-5人
        'itemId':11, 九龙湖舞蹈,非必选
        'itemId':12, 九龙湖健身,非必选
        'itemId':13, 九龙湖武术,非必选
        'itemId':14, 九龙湖跆拳道,非必选
        'itemId':15, 四牌楼羽毛球,1-3人
        'itemId':16, 四牌楼乒乓,1-3人
        'itemId':17, 四牌楼网球,1-3人
        """

    url2 = "http://yuyue.seu.edu.cn/eduplus/order/initEditOrder.do?sclId=1&dayInfo="+info['dayInfo']+"&itemId="+info['itemId']+"&time="+info["time"]
    # print(url2)
    # bro.execute_script("window.open()")
    # bro.switch_to.window(bro.window_handles[1])
    bro.get(url2)

    #处理篮球半场全场
    basketball=reserverdic["phonemate"]["halffull"]
    if basketball == 2:
        buttonhalffull = bro.find_elements_by_name("orderVO.useMode")
        buttonhalffull[1].click()
    #添加电话
    phonenumber = reserverdic["phonemate"]["phone"]
    input_phone = bro.find_element_by_id("phone")
    input_phone.clear()
    input_phone.send_keys(phonenumber)

    #添加好友
    framenum=0
    for eachmate in reserverdic["phonemate"]["mateid"]:
        framenum+=1
        addmates(eachmate,framenum,bro)
        time.sleep(1)



    #处理验证码
    screenshot = str(random.randint(1,100000))+'screenshot.png'
    validcodeshot = str(random.randint(1,100000))+'validateimage.png'
    bro.get_screenshot_as_file(screenshot)
    img = bro.find_element_by_xpath('//*[@id="fm"]/table/tbody/tr[6]/td[2]/img')
    left = int(img.location['x'])
    top = int(img.location['y'])
    right = int(img.location['x'] + img.size['width'])
    bottom = int(img.location['y'] + img.size['height'])

    # 通过Image处理图像
    im = Image.open(screenshot)
    im = im.crop((left, top, right, bottom))
    im.save(validcodeshot)

    img = Image.open(validcodeshot)
    validcode = pytesseract.image_to_string(img)
    # print(validcode)

    input_validcode = bro.find_element_by_id("validateCode")
    input_validcode.send_keys(validcode)
    button_reserve = bro.find_element_by_id("do-submit")
    button_reserve.click()

    os.remove(screenshot)
    os.remove(validcodeshot)
    time.sleep(1)



    try:
        alertcontent=bro.find_element_by_css_selector("[class='xubox_msg xubox_text']")
        if alertcontent.get_attribute("textContent"):
            print(alertcontent.get_attribute("textContent"), "预约失败")
            return 0
    except Exception:
        print("预约成功")
    return 1


def mmain():
    reserverdic1 = {
        "idpwd": {
            'ssid': 220184358,
            'pwd': "xwd2617976"
        },
        "info": {
            'dayInfo': "2019-09-02",
            'itemId': "7",
            'time': '12:00-13:00'
        },
        "phonemate": {
            "phone": 1885187965558,
            "mateid": [220184346],  # list 所有好友id
            "halffull": 1  # 1表示全场，2表示半场，非蓝球默认位1，或者空
        }
    }
    reserverdic2 = {
        "idpwd": {
            'ssid': 220184358,
            'pwd': "xwd2617976"
        },
        "info": {
            'dayInfo': "2019-09-03",
            'itemId': "8",
            'time': '17:00-18:00'
        },
        "phonemate": {
            "phone": 18851879658,
            "mateid": [220184348],  # list 所有好友id
            "halffull": 1  # 1表示全场，2表示半场，非蓝球默认位1，或者空
        }
    }
    groups=[reserverdic1,reserverdic2]

    pool = Pool()
    pool.map(main,groups)
    pool.map(main, groups)

def ppp():
    print(datetime.datetime.now())



if __name__ == '__main__':
    schedule.every(1).seconds.do(ppp)
    schedule.every().day.at('21:04').do(mmain)
    while True:
        schedule.run_pending()