from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__, template_folder='templates')

db = mysql.connector.connect(
    host="mysql-service",
    user="root",
    password="root",
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
    department_id = data['department_id']

    sql = "INSERT INTO employees (name, email, department_id) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, department_id))
    db.commit()
    return jsonify({"message": "Employee added successfully"}), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    cursor.execute("""
        SELECT e.id, e.name, e.email, e.department_id, d.name AS department_name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
    """)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "department_id": row[3],
            "department": row[4]
        })
    return jsonify(result)

@app.route('/departments', methods=['GET'])
def get_departments():
    cursor.execute("SELECT id, name FROM departments")
    rows = cursor.fetchall()
    result = [{"id": row[0], "name": row[1]} for row in rows]
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
