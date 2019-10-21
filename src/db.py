import mysql.connector
import logging
import os
import datetime

logger = logging.getLogger(__name__)
nohate_db = None
cursor = None


def init():
    global nohate_db
    global cursor
    try:
        nohate_db = mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            user="root",
            passwd=os.environ['MYSQL_ROOT_PASSWORD'],
            database=os.environ['MYSQL_DB_NAME']
        )
        cursor = nohate_db.cursor()
        return True

    except Exception as err:
        logger.warning("No database connection possible.")
        return False


def reconnect(retry_function, *args):
    nohate_db.reconnect(attempts=5, delay=2)
    logging.info("Reconnected to DB.")

    if nohate_db.is_connected():
        return retry_function(*args)


def fetch_last_entry():
    text_from_id_command = "SELECT id, text, lang FROM comments WHERE id = (SELECT MAX(id) FROM comments);"
    cursor.execute(text_from_id_command)

    return cursor.fetchone()


def duplicate_prev_id(text, lang):
    last_entry = fetch_last_entry()

    if last_entry is not None:

        prev_text = last_entry[1]
        prev_lang = last_entry[2]

        if text == prev_text and lang == prev_lang:
            return last_entry[0]

    return None


def insert_comment(text, lang, label=-1):
    try:
        duplicate_id = duplicate_prev_id(text, lang)

        if duplicate_id is None:

            current_datetime = datetime.datetime.now()
            insert_command = "INSERT INTO comments(text, date, label, lang) VALUES(%s, %s, %s, %s);"
            row_input = (text, current_datetime, label, lang)
            cursor.execute(insert_command, row_input)
            nohate_db.commit()

            return cursor.lastrowid

        else:
            logging.debug("Double entry, comment not inserted.")

            return duplicate_id

    except mysql.connector.errors.DatabaseError:
        return reconnect(insert_comment, text, lang, label)


def update_comment(comment_id, label):
    try:
        update_command = "UPDATE comments SET label = %s WHERE id = %s;"
        row_update = (label, comment_id)
        cursor.execute(update_command, row_update)
        nohate_db.commit()

        return comment_id

    except mysql.connector.errors.DatabaseError:
        return reconnect(insert_comment, comment_id, label)
