import pymysql

def connect():
    db = pymysql.connect(host='localhost', user='root', password = 'root', port = 3306, db = 'comment')
    cursor = db.cursor()
    return db, cursor
