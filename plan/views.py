# importing sqlite3
import sqlite3
# importing config
from . import config
# importing jwt_required
from flask_jwt import jwt_required
from flask import request, Response
import json

def plans_initialisation():
    conn=sqlite3.connect(config.plan_database_path)
    cur=conn.cursor()
    # initialise home_insurance table if not initialised already
    cur.execute('create table if not exists home_insurance (id int primary key, type varchar(20), price varchar(20))')
    try:
        cur.execute("insert into home_insurance values (1, 'Basic', '$38')")
        cur.execute("insert into home_insurance values (2, 'Gold', '$56')")
        cur.execute("insert into home_insurance values (3, 'Platinum', '$72')")
    except Exception as e:
        print(e)
    conn.commit()
    # initialise car_insurance table if not initialised already
    cur.execute('create table if not exists car_insurance (id int primary key, type varchar(20), price varchar(20))')
    try:
        cur.execute("insert into car_insurance values (1, 'Basic', '$48')")
        cur.execute("insert into car_insurance values (2, 'Gold', '$61')")
        cur.execute("insert into car_insurance values (3, 'Platinum', '$76')")
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

@jwt_required()
def get_user_plans():
    conn=sqlite3.connect(config.user_plan_database_path)
    cur=conn.cursor()
    user_data=json.loads(request.data)
    username=user_data['username']
    q="select * from user_plan where username='"+username+"'"
    res=cur.execute(q)
    res_d={}
    for ele in res:
        res_d['username']=ele[0]
        res_d['car_insurance_type']=ele[1]
        res_d['home_insurance_type']=ele[2]
    # get price of plans purchased by user
    conn=sqlite3.connect(config.plan_database_path)
    cur=conn.cursor()
    if res_d['car_insurance_type']!='None':
        q="select price from car_insurance where type='"+res_d['car_insurance_type']+"'"
        res=cur.execute(q)
        for ele in res:
            res_d['car_insurance_price']=ele[0]
    else:
        res_d['car_insurance_price']='None'

    
    if res_d['home_insurance_type']!='None':
        q="select price from home_insurance where type='"+res_d['home_insurance_type']+"'"
        res=cur.execute(q)
        for ele in res:
            res_d['home_insurance_price']=ele[0]
    else:
        res_d['home_insurance_price']='None'
    res=json.dumps(res_d)
    return res


@jwt_required()
def delete_insurance():
    conn=sqlite3.connect(config.user_plan_database_path)
    cur=conn.cursor()
    user_data=json.loads(request.data)
    username=user_data['username']
    item=user_data['item']
    if item=='car':
        q="update user_plan set car_insurance_plan_type='None' where username='"+username+"'"
        cur.execute(q)
        conn.commit()
        conn.close()
    if item=='home':
        q="update user_plan set home_insurance_plan_type='None' where username='"+username+"'"
        cur.execute(q)
        conn.commit()
        conn.close()
    return Response(status=201)

