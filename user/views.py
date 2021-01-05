# importing sqlite3
import sqlite3
# importing config file
from . import config
from flask_jwt import jwt_required

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
    conn=sqlite3.connect(config.user_database_path)
    cur=conn.cursor()
    username='a'
    q="select username from user where username='"+username+"'"
    user_data=cur.execute(q).fetchone()
    print(user_data)
    return 'yes'