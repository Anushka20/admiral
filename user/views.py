# importing sqlite3
import sqlite3
# importing config file
from . import config
from flask_jwt import jwt_required
from flask import request, Response
import json

# initialise user_plan database
def user_plan_initialisation():
    conn=sqlite3.connect(config.user_plan_database_path)
    cur=conn.cursor()
    q='create table if not exists user_plan (username varchar(30) primary key, car_insurance_plan_type varchar(20), home_insurance_plan_type varchar(20))'
    cur.execute(q)
    conn.commit()
    conn.close()

# get user profile
@jwt_required()
def user_profile():
    conn=sqlite3.connect(config.user_plan_database_path)
    cur=conn.cursor()
    request_data=json.loads(request.data)
    username=request_data['username']
    q="select username, car_insurance_plan_type, home_insurance_plan_type from user_plan where username='"+username+"'"
    user_data=cur.execute(q).fetchone()
    res_d={}
    res_d['username']=user_data[0]
    res_d['car_insurance_plan_type']=user_data[1]
    res_d['home_insurance_plan_type']=user_data[2]
    # connect to user.db
    conn=sqlite3.connect(config.user_database_path)
    cur=conn.cursor()
    q="select first_name, last_name, email from user where username='"+username+"'"
    user_data=cur.execute(q).fetchone()
    res_d['first_name']=user_data[0]
    res_d['last_name']=user_data[1]
    res_d['email']=user_data[2]
    res=json.dumps(res_d)
    return res

# update user profile
@jwt_required()
def update_profile():
    conn=sqlite3.connect(config.user_database_path)
    cur=conn.cursor()
    request_data=json.loads(request.data)
    username=request_data['username']
    first_name=request_data['first_name']
    last_name=request_data['last_name']
    email=request_data['email']
    q="update user set first_name='"+first_name+"', last_name='"+last_name+"', email='"+email+"' where username='"+username+"'"
    cur.execute(q)
    conn.commit()
    conn.close()
    return Response(status=201)
