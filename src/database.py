import mysql.connector

testDB = mysql.connector.connect(
    host = "localhost",
    user = "root",
    # ja ich weiss, gibt besser arten mit passwort umzugehen ^^
    passwd = "",
    database = "noHateDB",
    )

cursor = testDB.cursor()
# cursor.execute("CREATE DATABASE noHateDB")
# cursor.execute("CREATE TABLE testWords(sID INTEGER AUTO_INCREMENT PRIMARY KEY, command TEXT, date DATETIME, label TEXT)")
# cursor.execute("DROP TABLE testWords")

def insertRow(command, date, label):
    insertCommand = "INSERT INTO testWords(command, date, label) VALUES(%s, %s, %s)"
    input = (command, date, label)
    cursor.execute(insertCommand, input)
    testDB.commit()
