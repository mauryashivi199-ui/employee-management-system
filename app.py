from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="employee_db"
)

cursor = db.cursor()

# ✅ Add Employee (POST API)
@app.route('/employee', methods=['POST'])
def add_employee():
    data = request.get_json()

    name = data['name']
    email = data['email']
    department = data['department']

    sql = "INSERT INTO employees (name, email, department) VALUES (%s, %s, %s)"
    values = (name, email, department)

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Employee added successfully"}), 201


# ✅ Get All Employees (GET API)
@app.route('/employees', methods=['GET'])
def get_employees():
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "department": row[3]
        })

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
