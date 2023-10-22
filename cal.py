from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import datetime

db_connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='calculator'
)

app = Flask(__name__)
CORS(app)
db_cursor = db_connection.cursor()

@app.route('/record_history', methods=['POST'])
def record_history():
    data = request.get_json()
    expression = data.get('expression')
    result = data.get('result')

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_tuple = (current_time, expression, result)
    insert_query = "INSERT INTO alan_calculate VALUES (%s, %s, %s)"
    db_cursor.execute(insert_query, data_tuple)
    db_connection.commit()

    response_message = "Recorded successfully"
    return jsonify({"message": response_message})

@app.route('/fetch_calculations', methods=['GET'])
def fetch_calculations():
    db_cursor.execute("SELECT expression, result FROM alan_calculate ORDER BY time DESC LIMIT 10")
    data = db_cursor.fetchall()
    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(debug=True)
