from util import dbutil as util


def add(bookid, userid, comment):
    
    sql = 'insert into comment(bookid, userid, comment) values(%s, %s, %s)'
    db, cursor = util.connect()
    
    temp = 0
    try:
        temp = cursor.excute(sql, (bookid, userid, comment))
        db.commit()
    except:
        db.rollback()
    cursor.close()
    db.close()
    return temp

def getComment(bookid):
    
    sql = 'select username, comment  from user, comment where bookid = %s and user.userid = comment.userid'
    db, cursor = util.connect()
    
    temp = 0
    try:
        temp = cursor.execute(sql, (bookid))
        db.commit()
    except:
        db.rollback()
    cursor.close()
    db.close()
    
    datas = []
    data = {}
    if(temp != 0):
        results = cursor.fetchall()
        for result in results:
            data = {
                'username' : result[0], 
                'comment' :result[1]
            }
            datas.append(data)
    return temp, datas
    
if __name__ == "__main__":
    temp, datas = getComment(123)
    print(datas)
    