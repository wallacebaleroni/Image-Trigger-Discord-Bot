import os
import psycopg2


def connect_db():
    DATABASE_URL = os.environ.get('DATABASE_URL',
                                  "dbname=Image-Trigger-Discord-Bot user=postgres password=admin")

    conn = psycopg2.connect(DATABASE_URL)  # , sslmode='require')
    cursor = conn.cursor()

    return conn, cursor


def create_database():
    conn, cursor = connect_db()
    cursor.execute("""CREATE TABLE IF NOT EXISTS token (
                            token text  
                      )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS keyword (
                                chat_id numeric,
                                keyword text
                      )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS repo (
                                chat_id numeric,
                                repo text  
                      )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS eurotruck (
                                    time  numeric
                          )""")

    conn.commit()

    cursor.close()
    conn.close()


def set_keyword(keyword, chat_id):
    conn, cursor = connect_db()

    if get_keyword(chat_id) is not None:
        cursor.execute("""UPDATE keyword SET keyword='{0}' WHERE chat_id={1}""".format(keyword, chat_id))
    else:
        cursor.execute("""INSERT INTO keyword(chat_id, keyword) VALUES({0}, '{1}')""".format(chat_id, keyword))

    conn.commit()

    cursor.close()
    conn.close()


def get_keyword(chat_id):
    conn, cursor = connect_db()
    cursor.execute("""SELECT keyword FROM keyword WHERE chat_id={0}""".format(chat_id))
    keyword = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(keyword) == 0:
        return None
    else:
        keyword = keyword[0][0]

    return keyword


def set_imagerepo(repo, chat_id):
    conn, cursor = connect_db()

    if get_imagerepo(chat_id) is not None:
        cursor.execute("""UPDATE repo SET repo='{0}' WHERE chat_id={1}""".format(repo, chat_id))
    else:
        cursor.execute("""INSERT INTO repo(chat_id, repo) VALUES({0}, '{1}')""".format(chat_id, repo))

    conn.commit()

    cursor.close()
    conn.close()


def get_imagerepo(chat_id):
    conn, cursor = connect_db()
    cursor.execute("""SELECT repo FROM repo WHERE chat_id={0}""".format(chat_id))
    repo = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(repo) == 0:
        return None
    else:
        repo = repo[0][0]

    return repo


def get_time_eurotruck(tempo_agora):
    conn, cursor = connect_db()
    cursor.execute("""SELECT * FROM eurotruck""")
    eurotruck = cursor.fetchall()

    if len(eurotruck) > 0:
        cursor.execute("""INSERT INTO eurotruck VALUES({0})""".format(tempo_agora))
    elif len(eurotruck) == 1:
        for row in eurotruck:
            tempo_antigo = row[0]
            print(tempo_agora - tempo_antigo)
            if tempo_agora > tempo_antigo:
                cursor.execute("""UPDATE eurotruck SET repo={0}""".format(tempo_agora))

            cursor.close()
            conn.close()
            return tempo_agora - tempo_antigo

    cursor.close()
    conn.close()
    return 0
