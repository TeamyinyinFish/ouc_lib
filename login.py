from sql import user as user
import json

#登录：将微信号和微信名传入
def login(userid, username):
    temp = user.setUser(userid, username)
    if(temp == 1):
        return 1
    else:
        return -1

#绑定学号：将微信号、学号和密码传入
def setStuInfo(userid, stuid, stupwd):
    temp = user.setStuid(userid, stuid, stupwd)
    if(temp == 1):
        return 1
    else:
        return -1

#解除绑定：传入微信号
def clsStuInfo(userid):
    stuid = '123'
    stupwd = '123'
    return setStuInfo(userid, stuid, stupwd) 


#获取绑定的学号和密码：将微信号传入
def getStuInfo(userid):
    temp, data = user.getStuid(userid)
    if(temp == 1 and data['stuid'] != '123' and data['stupwd'] != '123'):
            stuinfo = json.dumps(data)
            return stuinfo
    else:
        return -1