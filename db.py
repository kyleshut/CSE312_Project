import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="cse312"
)

cursor = db.cursor()

def init():
    cursor.execute("CREATE DATABASE IF NOT EXISTS cse312")

def init_table():
    cursor.execute("CREATE TABlE accounts (username VARCHAR(255),password VARCHAR(255))")

def init_test_account():
    sql = "INSERT INTO accounts (username, password) VALUES(%s,%s)"
    val = ("root", "root")
    cursor.execute(sql, val)
    db.commit()

def add_account(user, passw):
    sql = "INSERT INTO accounts (username, password) VALUES(%s,%s)"
    val = (user,passw)
    cursor.execute(sql,val)
    db.commit()
    print("User: " + user + " has been created")

def account_exist(user):
    cursor.execute("SELECT * FROM accounts")
    for x in cursor.fetchall():
        if x[0] == user:
            return True
    return False

def remove_account(user):
    #Todo remove accounts
    pass

def login(user,passw):
    cursor.execute("SELECT * FROM accounts")
    for x in cursor.fetchall():
        if x[0] == user and x[0] == passw:
            return True
    return False

def show_db():
    cursor.execute("SELECT * FROM accounts")
    # fetch all the matching rows
    result = cursor.fetchall()
    for row in result:
        print(row)

