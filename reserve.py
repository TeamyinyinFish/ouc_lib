
import json
import requests
import re
import pandas as pd
postUrl = 'http://222.195.226.75/'
# payloadData数据
payloadData = {
    '__VIEWSTATE': '/wEPDwUKMTc2NzMyNTQ1NGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFBWNtZE9LtqxBv9c83wVjHLXRqLYs3JnYtsLSVmRCkjn83c6REoI=',
    '__VIEWSTATEGENERATOR': 'CA0B0334',
    '__EVENTVALIDATION': '/wEdAAQZBEzYt46+GxwUriR3XN3vY3plgk0YBAefRz3MyBlTcHY2+Mc6SrnAqio3oCKbxYbQfhPsHY8HS4bUZp7zVluV1ejwoub/jozWluO20t+rL3tdQZzCfCWb/A2NX4T5tcw=',
    'txtUserName': '16090033015',
    'txtPassword': 'wjw100521',
    'cmdOK.x': '0',
    'cmdOK.y': '0'
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3,',
    'Accept-Encoding': 'gzip, deflate',
    'Cache-Control': 'max-age=0',
    'Content-Length': '407',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ASP.NET_SessionId=54ktzagm43f32v5ladaboezy',
    'Host': '222.195.226.75',
    'Origin': 'http://222.195.226.75',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://222.195.226.75/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
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
    content = requests.post(postUrl, data=payloadData, headers=headers)
    print(content.text)
