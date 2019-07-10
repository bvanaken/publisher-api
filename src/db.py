import mysql.connector
import logging
import os
print()

nohate_db = mysql.connector.connect(
    host=os.environ['MYSQL_HOST'],
    user="root",
    passwd=os.environ['MYSQL_ROOT_PASSWORD'],
    database=os.environ['MYSQL_DB_NAME']
)

cursor = nohate_db.cursor()

logger = logging.getLogger(__name__)


def duplicate_prev_id(text, lang):
    text_from_id_command = "SELECT id, text, lang FROM comments WHERE id = (SELECT MAX(id) FROM comments);"
    cursor.execute(text_from_id_command)

    result = cursor.fetchone()

    prev_text = result[1]
    prev_lang = result[2]

    logging.debug("text_from_id_command: " + str(result))

    if text == prev_text and lang == prev_lang:
        return result[0]
    else:
        return None


def insert_comment(text, date, lang, label=-1):
    duplicate_id = duplicate_prev_id(text, lang)

    if duplicate_id is None:

        insert_command = "INSERT INTO comments(text, date, label, lang) VALUES(%s, %s, %s, %s);"
        row_input = (text, date, label, lang)
        cursor.execute(insert_command, row_input)
        nohate_db.commit()

        return cursor.lastrowid

    else:
        logging.debug("Double entry, comment not inserted.")

        return duplicate_id


def update_comment(comment_id, label):
    update_command = "UPDATE comments SET label = %s WHERE id = %s;"
    row_update = (label, comment_id)
    cursor.execute(update_command, row_update)
    nohate_db.commit()

    return comment_id
