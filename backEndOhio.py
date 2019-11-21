from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_restful import Api, Resource, reqparse
import pymysql
from functools import partial
import os

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('Tarefa', type=str)

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
        return cursor
        # for result in cursor:
        #     print(result)

connection = pymysql.connect(
    host=endpoint,
    user='AdminFrancato',
    password=senhaDB1,
    database='Cloud')

db = partial(run_db_query, connection)


class Tarefa(Resource):
    def get(self):
        dictTarefas = {}
        a = db('SELECT * FROM Tarefas ORDER BY IDTarefa DESC')
        for i in a:
            dictTarefas[i[0]] = i[1]
        return jsonify(dictTarefas)

    def post(self):
        request.get_json(force=True)
        args = parser.parse_args()
        tarefa =  str(args['Tarefa'])
        connection.cursor().execute("INSERT INTO Tarefas (Nome) values (%s)", [tarefa])
        connection.cursor().execute('COMMIT;')
        return jsonify({"Status": 200})


class Nada(Resource):
    def get(self):
        return "Hello WOrld"


class TarefaId(Resource):
    def get(self, id):
        a = db('SELECT Nome FROM Tarefas WHERE IDTarefa = %s', [id])
        for i in a:
            tarefa = i
        return jsonify({"Tarefa": tarefa[0]})

    def put(self, id):
        request.get_json(force=True)
        args = parser.parse_args()
        tarefa =  str(args['Tarefa'])
        try:
            connection.cursor().execute("INSERT INTO Tarefas (IDTarefa, Nome) values (%s,%s)", [id, tarefa])
            connection.cursor().execute('COMMIT;')
        except:
            return jsonify({"Erro": "Ja existe uma tarefa com esse ID"})
        return jsonify({"Status": 200})

    def delete(self, id):
        try:
            connection.cursor().execute("DELETE FROM Tarefas WHERE IDTarefa = %s", [id])
            connection.cursor().execute('COMMIT;')
            return jsonify({"Status": 200})
        except:
            return jsonify({"Erro": "ID inexistente"})
            

class HealthCheck(Resource):
    def get(self):
        return  jsonify({"Status": 200})

api.add_resource(Tarefa, '/Tarefa/')
api.add_resource(HealthCheck, '/HealthCheck')
api.add_resource(TarefaId, '/Tarefa/<int:id>')
api.add_resource(Nada, '/')


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=8080)
