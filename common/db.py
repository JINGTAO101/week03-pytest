import pymysql

def query(sql,args=None,):
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="qa123456",
        database="qa_practice",
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cur:
            cur.execute(sql,args or ())
            return cur.fetchall()
    finally:
        conn.close()

def execute(sql, args=None):
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="qa123456",
        database="qa_practice",
    )
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

