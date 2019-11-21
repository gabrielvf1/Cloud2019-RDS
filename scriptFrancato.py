import pymysql
from functools import partial
import os

f= open("/home/dados.txt","r")
dados = f.readlines()
for i in dados:
    linha = i.split()
    if linha[0] == 'endpoint:':
        endpoint = linha[1]
    if linha[0] == 'senha:':
        senhaDB1 = linha[1]

def run_db_query(connection, query, args=None):
    with connection.cursor() as cursor:
        print('Executando query:')
        cursor.execute(query, args)
        for result in cursor:
            print(result)

con = pymysql.connect(
    host=endpoint,
    user='AdminFrancato',
    password=senhaDB1
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
con.cursor().execute('COMMIT;')

connection = pymysql.connect(
    host=endpoint,
    user='AdminFrancato',
    password=senhaDB1,
    database='Cloud')
db = partial(run_db_query, connection)
connection.cursor().execute('INSERT INTO Tarefas (Nome) values ("Dormir")')
connection.cursor().execute('INSERT INTO Tarefas (Nome) values ("Andar")')
connection.cursor().execute('INSERT INTO Tarefas (Nome) values ("Jogar")')
connection.cursor().execute('COMMIT;')
db('SELECT * FROM Tarefas')
