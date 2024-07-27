import sqlite3


dbfile = 'data.db'
def create_table(table_name):
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()

        create_table = "CREATE TABLE {} (user_id int, fans_id int, username text, img_url text)".format(table_name)
        cursor.execute(create_table)

        conn.commit()
        conn.close()
    except Exception as e:
        print('crteate table error')
        print(e)

def insert_table(table_name, user_id, fans_id, username, img_url):
    insert_table = ""
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        insert_table = 'INSERT INTO {table_name} (user_id, fans_id, username, img_url) VALUES ( {id}, {fans_id}, "{un}", "{url}")'.format(table_name=table_name, id=user_id, fans_id=fans_id, un=username, url=img_url)
        cursor.execute(insert_table)
        conn.commit()
        conn.close()
    except Exception as e:
        print('insert table error')
        print(e)
        print(insert_table)


