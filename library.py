"""
_*_coding:utf-8 _*_

@Time    :2019/11/7 9:16
@Author  :csqin 
@FileName: library.py
@Software: PyCharm

"""
import json
import requests
import re
import pandas as pd
postUrl = 'http://222.195.226.30/opac/ajax_search_adv.php'
# payloadData数据
payloadData = {
    'afnPriceStr': 10,
    'currency':'USD',
    'productInfoMapping': {
        'asin': 'B072JW3Z6L',
        'dimensionUnit': 'inches',
    }
}
# 请求头设置
payloadHeader = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/json',
    'DNT': '1',
    'Origin': 'http://222.195.226.30',
    'Referer': 'http://222.195.226.30/opac/search_adv.php',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',

}
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,fr-FR;q=0.8,fr;q=0.7,zh-TW;q=0.6,en;q=0.5',
'Connection': 'keep-alive',
'Cookie': '',
'DNT': '1',
'Host': '222.195.226.30',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}
header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}


def search_book(fieldCode,keyword,page):
        dumpJsonData = '{"searchWords":[{"fieldList":[{"fieldCode":"' + fieldCode + '","fieldValue":"' + keyword + '"}]}],' \
                       '"filters":[],"limiter":[],' '"sortField":"relevance","sortType":"desc","pageSize":20,"pageCount":' \
                        '"' + page + '","first":true}'
        res= {"total_records":"","list":""}
        content = requests.post(postUrl, data=dumpJsonData.encode('utf-8'), headers=payloadHeader)
        # 查询总的结果数
        res["total_records"] = json.loads(content.text)['total']
        # 如果获取的记录大于一页
        booklist = json.loads(content.text)['content']
        # 给每一本书附上可借阅的数量,还有图片
        for i in range(len(booklist)):
            urlstatus = 'http://222.195.226.30/opac/ajax_isbn_marc_no.php?marc_no=' \
                        + booklist[i]['marcRecNo'] + '&rdm=13515&isbn=' + \
                        booklist[i]['isbn']
            getr = requests.get(url=urlstatus, headers=headers)
            # 可借阅的数量
            num = json.loads(getr.text)['lendAvl']
            cover_image = json.loads(getr.text)['image']
            if cover_image == "":
                booklist[i]['cover_image'] = ""
            else:
                booklist[i]['cover_image'] = cover_image
            # print(cover_image)
            # 书的可借数量
            booklist[i]['sum'] = re.findall(r">(\d+)<",num)[0]
            booklist[i]['available'] = num[-1]
            if 'callNo' in booklist[i].keys():
                del booklist[i]['callNo']
            if 'docTypeName' in booklist[i].keys():
                del booklist[i]['docTypeName']
            if 'num' in booklist[i].keys():
                del booklist[i]['num']
            res["list"] = booklist
        print(res)
        return res
def get_bookDetail(bookID):
    bookDetail_url = "http://222.195.226.30/opac/item.php?marc_no=" + str(bookID)
    content = requests.get(bookDetail_url,headers = header)
    content = pd.DataFrame(pd.read_html(content.text)[0]).fillna('')
    print(len(content))
    print(content.columns.size)
    print()
    res = {"have_info":"1","bookAvailableDetail":""}
    bookAvailableDetail = []
    # 如果有藏书的话
    if content.columns.size != 1:
        for i in range(1,len(content)):
            temp = content.iloc[i,]
            item = {"number": "", "barcode": "", "date": "", "location": "", "status": ""}
            for j in range(5):
                item["number"] = str(temp[0])
                item["barcode"] = str(temp[1])
                item["date"] = str(temp[2])
                item["location"] = str(temp[3])
                item["status"] = str(temp[4])
            bookAvailableDetail.append(item)
        res["bookAvailableDetail"] = bookAvailableDetail
        return res
    else:
        res["have_info"] = "0"
        return res
if __name__ == '__main__':
    search_book('02','操作系统','1')
