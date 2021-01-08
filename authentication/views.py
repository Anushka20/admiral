# importing request, reditect, url_for, render_template
from flask import request, redirect, url_for, render_template
# importing requests
import requests
# importing json
import json
# for database interaction
import sqlite3
from . import config
# for authentication
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

def users_initialisation():
    conn=sqlite3.connect(config.user_database_path)
    cur=conn.cursor()
    # create user table if not already present
    cur.execute('create table if not exists user (username varchar(30) primary key, password varchar(30), first_name varchar(30) default "", last_name varchar(30) default "", email varchar(30) default "")')
    conn.commit()
    conn.close()

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
    conn=sqlite3.connect(config.user_database_path)
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
    conn=sqlite3.connect(config.user_database_path)
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
    if request.method=='GET':
        return render_template('home.html')
    form_data=request.form
    username=form_data['username']
    password=form_data['password']
    # connect to database
    conn=sqlite3.connect(config.user_database_path)
    cur=conn.cursor()
    # create new user
    try:
        q="insert into user values ('" + username + "','" + password + "', '', '', '')"
        cur.execute(q)
        conn.commit()
        conn.close()
        # get access token for the user
        res=requests.post('http://127.0.0.1:5000/auth',data=json.dumps({'username':username,'password':password}), headers={'content-type': 'application/json'})
        res=res.json()
        # create entry into user_plan database for new user
        conn=sqlite3.connect(config.user_plan_database_path)
        cur=conn.cursor()
        q="insert into user_plan values ('"+username+"', 'None', 'None')"
        cur.execute(q)
        conn.commit()
        conn.close()
        # access token
        access_token=res['access_token']
        return render_template('home.html',access_token=access_token, username=username)
    except Exception as e:
        print(e)
        return 'Username already exists!'
    
    

# login function
def login():
    if request.method=='GET':
        return render_template('home.html')
    # connect to database
    conn=sqlite3.connect(config.user_database_path)
    cur=conn.cursor()
    form_data=request.form
    # get submitted username and password
    username=form_data['username']
    password=form_data['password']
    q="select username, password from user where username='" + username + "'"
    res=cur.execute(q)
    for user in res:
        user_name=user[0]
        pass_word=user[1]
        if password==pass_word:
            # password is correct
            # get access token for the user
            res=requests.post('http://127.0.0.1:5000/auth',data=json.dumps({'username':username,'password':password}), headers={'content-type': 'application/json'})
            res=res.json()
            # access token
            access_token=res['access_token']
            return render_template('home.html',access_token=access_token, username=username)
    return render_template('home.html')
