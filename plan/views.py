# importing sqlite3
import sqlite3
# importing config
from . import config
# importing jwt_required
from flask_jwt import jwt_required
from flask import request
import json

def plans_initialisation():
    conn=sqlite3.connect(config.plan_database_path)
    cur=conn.cursor()
    # initialise home_insurance table if not initialised already
    cur.execute('create table if not exists home_insurance (id int primary key, type varchar(20))')
    try:
        cur.execute("insert into home_insurance values (1, 'basic')")
        cur.execute("insert into home_insurance values (2, 'gold')")
        cur.execute("insert into home_insurance values (3, 'advance')")
    except Exception as e:
        print(e)
    conn.commit()
    # initialise car_insurance table if not initialised already
    cur.execute('create table if not exists car_insurance (id int primary key, type varchar(20))')
    try:
        cur.execute("insert into car_insurance values (1, 'basic')")
        cur.execute("insert into car_insurance values (2, 'gold')")
        cur.execute("insert into car_insurance values (3, 'advance')")
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()

@jwt_required()
def update_car_insurance_plan():
    conn=sqlite3.connect(config.user_plan_database_path)
    cur=conn.cursor()
    user_data=json.loads(request.data)
    plan_type=user_data['plan_type']
    username=user_data['username']
    q="update user_plan set car_insurance_plan_type='"+plan_type+"' where username='"+username+"'"
    cur.execute(q)
    q="select * from user_plan where username='"+username+"'"
    res=cur.execute(q)
    for ele in res:
        print(ele)
    conn.commit()
    conn.close()
    return 'updated'

@jwt_required()
def update_home_insurance_plan():
    conn=sqlite3.connect(config.user_plan_database_path)
    cur=conn.cursor()
    user_data=json.loads(request.data)
    plan_type=user_data['plan_type']
    username=user_data['username']
    q="update user_plan set home_insurance_plan_type='"+plan_type+"' where username='"+username+"'"
    cur.execute(q)
    q="select * from user_plan where username='"+username+"'"
    res=cur.execute(q)
    for ele in res:
        print(ele)
    conn.commit()
    conn.close()
    return 'updated'
