from util import dbutil as util

def search(userid):
    
    sql = 'select * from user where userid = %s'
    db, cursor = util.connect()
    
    temp = 0
    try:
        temp = cursor.execute(sql, (userid))
        db.commit()
    except:
        db.rollback()
    cursor.close()
    db.close()
    return temp


def setUser(userid, username):
    
    stuid = '123'
    stupwd = '123'
    sql = 'insert into user(userid, username, stuid, stupwd) values(%s, %s, %s,%s)'
    db, cursor = util.connect()
    
    temp = 0
    try:
        if(search(userid)!=0):
            temp = -1
        else:
            temp = cursor.execute(sql,(userid, username, stuid, stupwd))
            db.commit()
    except:
        db.rollback()
    cursor.close()
    db.close()
    return temp
    
def setStuid(userid, stuid, stupwd):
    
    sql = 'update user set stuid=%s, stupwd=%s where userid = %s'
    db, cursor = util.connect()
    
    temp = 0
    try:
        if(search(userid)==0):
            temp = -1
        else:
            temp = cursor.execute(sql,(stuid, stupwd, userid))
            db.commit()
    except:
        db.rollback()
    cursor.close()
    db.close()
    return temp
    
def getStuid(userid):
    
    sql = 'select stuid, stupwd from user where userid = %s'
    db, cursor = util.connect()
    
    temp = 0
    try:
        if(search(userid)==0):
            temp = -1
        else:
            temp = cursor.execute(sql, (userid))
            db.commit()
    except:
        db.rollback()
    cursor.close()
    db.close()
    data = {}
    if(temp == 1):
        result = cursor.fetchall()
        data = {
            'stuid' : result[0][0], 
            'stupwd' : result[0][1]
        }
    return temp, data
    