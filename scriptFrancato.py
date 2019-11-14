import pymysql
from functools import partial

def run_db_query(connection, query, args=None):
    with connection.cursor() as cursor:
        print('Executando query:')
        cursor.execute(query, args)
        for result in cursor:
            print(result)

con = pymysql.connect(
    host='localhost',
    user='root',
    password=''
    )

con.cursor().execute('DROP DATABASE IF EXISTS Cloud')
con.cursor().execute('CREATE DATABASE Cloud')
con.cursor().execute('DROP TABLE IF EXISTS `Cloud`.`Tarefas`')
con.cursor().execute('''
CREATE TABLE IF NOT EXISTS `Cloud`.`Tarefas` (
 `IDTarefa` INT NOT NULL AUTO_INCREMENT,
 `Nome` VARCHAR(255) NOT NULL,
 PRIMARY KEY (IDTarefa))''')
# ''')

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='cloud')
db = partial(run_db_query, connection)
connection.cursor().execute('INSERT INTO Tarefas (Nome) values ("Dormir")')
connection.cursor().execute('INSERT INTO Tarefas (Nome) values ("Andar")')
connection.cursor().execute('INSERT INTO Tarefas (Nome) values ("Jogar")')