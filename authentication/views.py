# importing request
from flask import request
# importing json
import json
# for database interaction
import sqlite3
# database path
from . import config
# for authentication
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

# user class
class User(object):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

    def __str__(self):
        return "User(username='%s')" % self.username

def authenticate(username, password):
    # connect to database
    conn=sqlite3.connect(config.database_path)
    cur=conn.cursor()
    q="select username, password from user where username='" + username + "'"
    res=cur.execute(q)
    user_name=None
    for user in res:
        user_name=user[0]
        pass_word=user[1]
    if user_name:
        user = User(user_name, pass_word)
    else:
        return None
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_name = payload['identity']
    # connect to database
    conn=sqlite3.connect(config.database_path)
    cur=conn.cursor()
    q="select username, password from user where username='" + user_name + "'"
    res=cur.execute(q)
    for user in res:
        user_name=user[0]
        pass_word=user[1]
    user = User(user_name, pass_word)
    if user:
        return user
    return None


# signup function
def signup():
    data=json.loads(request.data)
    username=data['username']
    password=data['password']
    # connect to database
    conn=sqlite3.connect(config.database_path)
    cur=conn.cursor()
    # create user table if not already present
    cur.execute('create table if not exists user (username varchar(30) primary key, password varchar(30))')
    conn.commit()
    # create new user
    try:
        q="insert into user values ('" + username + "','" + password + "')"
        cur.execute(q)
        conn.commit()
    except Exception as e:
        print('User not created',e)
    finally:
        conn.close()
    return 'hello'

# login function
def login():
    # connect to database
    conn=sqlite3.connect(config.database_path)
    cur=conn.cursor()
    data=json.loads(request.data)
    # get submitted username and password
    username=data['username']
    password=data['password']
    q="select username, password from user where username='" + username + "'"
    res=cur.execute(q)
    for user in res:
        print(user)
    return 'hi'