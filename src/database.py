
import mysql.connector

nohate_db = mysql.connector.connect(
    host = "localhost",
    port = "3308",
    user = "root",
    passwd = "freiheit2018",
    database = "nohate_db",
    )

cursor = nohate_db.cursor()
new_table = cursor.execute("CREATE TABLE comments(sID INTEGER AUTO_INCREMENT PRIMARY KEY, command TEXT, date DATETIME)")

def insert_comment(command, date, label):
    insert_command = "INSERT INTO comments(command, date, label) VALUES(%s, %s, %s)"
    row_input = (command, date, label)
    cursor.execute(insert_command, row_input)
    nohate_db.commit()


# "Create database/table as follows:"
# cursor.execute("CREATE DATABASE nohate_db")
# cursor.execute("CREATE TABLE comments(sID INTEGER AUTO_INCREMENT PRIMARY KEY, command TEXT, date DATETIME, label TEXT)")
# cursor.execute("DROP TABLE comments")
