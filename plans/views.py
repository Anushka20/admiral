# importing sqlite3
import sqlite3
# importing config
from . import config

def plans_initialisation():
    conn=sqlite3.connect(config.plan_database_path)
    cur=conn.cursor()
    cur.execute('create table if not exists home_insurance (id int primary key, type varchar(20))')
    try:
        cur.execute("insert into home_insurance values (1, 'basic')")
        cur.execute("insert into home_insurance values (2, 'gold')")
        cur.execute("insert into home_insurance values (3, 'advance')")
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()
