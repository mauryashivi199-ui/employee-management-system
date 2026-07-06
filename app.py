from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import date

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

# Mark or update attendance for an employee on a given date
@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    employee_id = data['employee_id']
    att_date = data.get('date', str(date.today()))
    status = data.get('status', 'Present')

    sql = """
        INSERT INTO attendance (employee_id, date, status)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE status = VALUES(status), marked_at = CURRENT_TIMESTAMP
    """
    cursor.execute(sql, (employee_id, att_date, status))
    db.commit()
    return jsonify({"message": "Attendance marked successfully"}), 201

# Get full attendance history (all employees, all dates)
@app.route('/attendance', methods=['GET'])
def get_attendance():
    cursor.execute("""
        SELECT a.id, a.employee_id, e.name, a.date, a.status
        FROM attendance a
        JOIN employees e ON a.employee_id = e.id
        ORDER BY a.date DESC
    """)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "employee_id": row[1],
            "employee_name": row[2],
            "date": str(row[3]),
            "status": row[4]
        })
    return jsonify(result)

# Get attendance history for one specific employee
@app.route('/attendance/<int:employee_id>', methods=['GET'])
def get_employee_attendance(employee_id):
    cursor.execute("""
        SELECT id, date, status FROM attendance
        WHERE employee_id = %s ORDER BY date DESC
    """, (employee_id,))
    rows = cursor.fetchall()
    result = [{"id": row[0], "date": str(row[1]), "status": row[2]} for row in rows]
    return jsonify(result)

# Get today's attendance status for every employee (shows Unmarked if none yet)
@app.route('/attendance/today', methods=['GET'])
def get_today_attendance():
    today = str(date.today())
    cursor.execute("""
        SELECT e.id, e.name, a.status
        FROM employees e
        LEFT JOIN attendance a ON e.id = a.employee_id AND a.date = %s
    """, (today,))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "employee_id": row[0],
            "name": row[1],
            "status": row[2] if row[2] else "Unmarked"
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
