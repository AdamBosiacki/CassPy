from flask import Flask, jsonify, request
from cassandra.cluster import Cluster


app = Flask(__name__)

cluster = Cluster(['localhost'])
session = cluster.connect('uni')


@app.route('/api/university', methods=['POST'])
def create_uni():
    data = request.get_json()
    qp = 'INSERT INTO university (name, score, typ) VALUES (?, ?, ?)'
    session.execute(qp, (data['value1'], data['value2'], data['value3']))
    return jsonify({'message': 'Successful insert'})

@app.route('/api/university', methods=['GET'])
def get_unis():
    min_score = request.args.get('min_score')
    max_score = request.args.get('max_score')

    query = "SELECT * FROM university WHERE score >= ? AND score <= ?"
    result = session.execute(query, (min_score, max_score))

    unis = []
    for row in result:
        university = {
            'id': row.id,
            'name': row.name,
            'score': row.score,
            'type': row.type
        }
        unis.append(university)

    return jsonify(unis)

if __name__ == '__main__':
    app.run()
