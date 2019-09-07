import json
import re
import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
from urllib.parse import unquote
from multiprocessing import Pool
import os
from hashlib import md5
def get_page(offset):
    key={
        'type':'image',
        'dpr':3,
        'id':offset,
    }
    url = 'https://api.tuwan.com/apps/Welfare/detail?' + urlencode(key)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求页出错", url)
        return None
def getUrl(html):

    pattern1 = re.compile('"thumb":(.*?)}', re.S)
    result = re.findall(pattern1, html)
    bigUrl=result[0]
    bigUrl=bigUrl.replace('"','').replace('\\','')
    pattern2 = re.compile('(http.*?.+jpg),', re.S)
    result2 = re.findall(pattern2, bigUrl)
    bigUrl=result2[0]

    pattern3 = re.compile('(http.*?==.*?\.jpg)', re.S)
    result3=re.findall(pattern3,result[3])
    smallUrl = []
    for item in result3:
        # print(item.replace('\\',''))
        smallUrl.append(item.replace('\\',''))
    return (bigUrl,smallUrl)

def  findReplaceStr(url):
    pattern = re.compile('.*?thumb/jpg/+(.*?wx+)(.*?)(/u/.*?).jpg', re.S)
    result = re.match(pattern, url)
    return result.group(2)

def getBigImageUrl(url,replaceStr):
    pattern = re.compile('.*?thumb/jpg/+(.*?wx+)(.*?)(/u/.*?).jpg', re.S)
    result = re.match(pattern, url)
    newurl='http://img4.tuwandata.com/v3/thumb/jpg/'+result.group(1)+replaceStr+ result.group(3)
    return newurl
def save_image(content,offset):

    path='{0}'.format(os.getcwd()+'\imagenew\\'+str(offset))
    file_path='{0}\{1}.{2}'.format(path,md5(content).hexdigest(), 'jpg')
    print(file_path)

    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()
def download_images(url,offset):
    print('downloading:',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content,offset)
        return None
    except RequestException:
        print("请求图片出错",url)
        return None

def download(bigImageUrl,smallImageUrl,offset):
    replaceStr = findReplaceStr(bigImageUrl)
    for url in smallImageUrl:
        download_images(getBigImageUrl(url,replaceStr),offset)

# if __name__ == '__main__':
#
#     offset=1473
#     html = get_page(offset)
#     urls = getUrl(html)
#     download(urls[0],urls[1],offset)

def main(offset):
    try:
        html = get_page(offset)
        urls = getUrl(html)
        download(urls[0], urls[1], offset)
        return None
    except Exception:
        print("地址出错:",offset)
        return None

if __name__ == '__main__':
    groups = [x  for x in range(1500,2000)]
    pool = Pool()
    pool.map(main,groups)



