import time
import requests
import json
import urllib.request
import os
import re
from PIL import Image
from io import BytesIO
from pylab import *
from bs4 import BeautifulSoup
import pandas as pd

seatslog_url="http://222.195.226.75/Default.aspx"
seatsForm_url="http://222.195.226.75/Florms/FormSYS.aspx"
seats_url = "http://222.195.226.75/FunctionPages/SeatBespeak/BespeakSeat.aspx"
imag_url="http://222.195.226.75/FunctionPages/Statistical/LibraryUsedStat.aspx"

def find_seats(username, password):
    sessiona = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    response = sessiona.get(url =seatslog_url, headers=headers)

    data = {
        "__VIEWSTATE":"/wEPDwUKMTc2NzMyNTQ1NGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFBWNtZE9LtqxBv9c83wVjHLXRqLYs3JnYtsLSVmRCkjn83c6REoI=",
        "__VIEWSTATEGENERATOR": "CA0B0334",
        "__EVENTVALIDATION":"/wEdAAQZBEzYt46+GxwUriR3XN3vY3plgk0YBAefRz3MyBlTcHY2+Mc6SrnAqio3oCKbxYbQfhPsHY8HS4bUZp7zVluV1ejwoub/jozWluO20t+rL3tdQZzCfCWb/A2NX4T5tcw=",
        "txtUserName": username,
        "txtPassword": password,
        "cmdOK.x":"38",
        "cmdOK.y":"19"
    }

    content = sessiona.post(url=seatsForm_url, data=data, headers=headers)
    seats_soup = BeautifulSoup(content.text, 'lxml')
    #print(content.text)
    #tags = seats_soup.find_all('div', class_='x-grid3-body', id='ext-gen45')
    #print(tags)
    if seats_soup.findAll(name = "form",attrs={"name":"frm_login"}) ==[]:
        cookiejar = sessiona.cookies
        # 获取当前页面的cookie以便用来访问当前页面的其它页面
        cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
    #print(cookiejar)
    #print(cookiedict)

    #now_seats = requests.post(url=seatsForm_url, cookies=cookiedict)
    #print(now_seats.text)
    #soup = BeautifulSoup(now_seats.text, 'html.parser')
    #print(soup.select('jpg'))


    imag_seats=requests.get(url=imag_url, cookies=cookiedict)
    #print(imag_seats.text)
    soup = BeautifulSoup(imag_seats.text, 'html.parser')
    r=soup.select('img')
    for each in r:
        #print(each)
        a=str(each)
        #print(re.findall(r"src=(.+?) style",a))
        imaglao_url="http://222.195.226.75"+str(re.findall(r"src=(.+?) style",a).pop()).replace('"','').replace('amp;','')
        #print(imaglao_url)

    r=requests.get(url=imaglao_url, cookies=cookiedict)
    with open('崂山图书馆.jpg','wb') as f:
        f.write(r.content)


if __name__ == "__main__":
    find_seats('17020013018', '17020013018')