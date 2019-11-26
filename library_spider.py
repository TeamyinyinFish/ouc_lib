import time
import requests
from PIL import Image
from io import BytesIO
from pylab import *
from bs4 import BeautifulSoup
import pandas as pd
def captcha(data):
    with open('captcha.jpg', 'wb') as fp:
        fp.write(data)
    # time.sleep(1)
    img = Image.open(BytesIO(data))
    plt.imshow(img)
    axis('off')
    plt.show()
    return input("请输入验证码：")
login_url = "http://222.195.226.30/reader/login.php"
captcha_url = "http://222.195.226.30/reader/captcha.php"
library_url = "http://222.195.226.30/reader/redr_verify.php"
bookList_url = "http://222.195.226.30/reader/book_lst.php"
renew_url = "http://222.195.226.30/reader/ajax_renew.php"
def login(username, password):
    # 构建一个保存Cookie值的session对象
    sessiona = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    # 先获取页面信息，找到需要POST的数据（并且已记录当前页面的Cookie）
    response = sessiona.get(url = login_url, headers=headers)

    response = sessiona.get(url =captcha_url, headers=headers)
    data = {
        "number": username,
        "passwd": password,
        "select": 'cert_no',
        "captcha": captcha(response.content)
    }
    # 如果验证码错误怎么办
    myLibrary = sessiona.post(url = library_url, data=data, headers=headers)
    myLibrary_soup = BeautifulSoup(myLibrary.text, 'lxml')
    if myLibrary_soup.findAll(name = "form",attrs={"name":"frm_login"}) ==[]:
        cookiejar = sessiona.cookies
        # 获取当前页面的cookie以便用来访问当前页面的其它页面
        cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
        # print(cookiejar)
        # print(cookiedict)
        # 获取我的借阅页面
        now_borrow = requests.get(url=bookList_url, cookies=cookiedict)
        # 获取我的借阅列表
        book_list = pd.read_html(now_borrow.text)[0]
        print("==============已借阅列表==============\n",book_list)
        bookList_soup = BeautifulSoup(now_borrow.text,'lxml')
        renew_params = bookList_soup.findAll(name="input",attrs={"title":"renew"})
        # 共几本书
        n_books = len(renew_params)
        # 每本书如果续借的参数
        params = [{"bar_code":'', "check":'',"captcha":'',"time":None}]*n_books
        # 遍历每个续借input的属性，提取需要的参数bar_code 和 check
        for i,renew_param in enumerate(renew_params):
            needed_param = re.findall("'([a-zA-Z0-9]*)'", renew_param['onclick'])
            params[i]["bar_code"] = needed_param[0]
            params[i]["check"] = needed_param[1]
        # print(renew_params)
        # print(params)
        print("当前你一共借阅了{}本书".format(n_books))
        renew_num = int(input("续借第几本?请输入："))

        # 点击续借按钮也需要输入验证码
        response = requests.get(url=captcha_url, cookies=cookiedict)

        # 完善续借所用的参数(条码号，校验码，验证码，时间戳)
        params[renew_num - 1]['captcha'] = captcha(response.content)
        params[renew_num - 1]['time'] = int(round(time.time() * 1000))
        renew = requests.get(url=renew_url, params = params[renew_num - 1], cookies=cookiedict)

        # 返回续借成功或达到最大次数
        print(re.findall(r'>(.*)<',renew.text)[0])

    else:
        isLogin_table = pd.read_html(myLibrary.text)[0]
        wrong_info = isLogin_table[1][6]
        print(wrong_info)
    # print(response.text)
    renew = "http://222.195.226.30/reader/ajax_renew.php?bar_code=3110342&check=69B04C17&captcha=LCHK&time=1572526897722"
    #print(now_borrow.text)


if __name__ == "__main__":
    login('学号', '密码')
