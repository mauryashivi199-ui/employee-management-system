from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__, template_folder='templates')

db = mysql.connector.connect(
    host="172.17.0.1",
    user="root",
    password="Test@1234",
    database="mydb"
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    name = data['name']
    email = data['email']
    department = data['department']
    sql = "INSERT INTO employees (name, email, department) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, department))
    db.commit()
    return jsonify({"message": "Employee added successfully"}), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({"id": row[0], "name": row[1], "email": row[2], "department": row[3]})
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
