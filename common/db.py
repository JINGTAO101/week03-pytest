import os
import pymysql

def _connect(**kwargs):
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user="root",
        password="qa123456",
        database="qa_practice",
        **kwargs,
    )

def query(sql,args=None,):
    conn = _connect(cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cur:
            cur.execute(sql,args or ())
            return cur.fetchall()
    finally:
        conn.close()

def execute(sql, args=None):
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args or ())
            last_id = cur.lastrowid
        conn.commit()
        return last_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

