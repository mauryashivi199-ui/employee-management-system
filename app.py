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

@app.route('/attendance/<int:employee_id>', methods=['GET'])
def get_employee_attendance(employee_id):
    cursor.execute("""
        SELECT id, date, status FROM attendance
        WHERE employee_id = %s ORDER BY date DESC
    """, (employee_id,))
    rows = cursor.fetchall()
    result = [{"id": row[0], "date": str(row[1]), "status": row[2]} for row in rows]
    return jsonify(result)

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

# Apply for leave
@app.route('/leave', methods=['POST'])
def apply_leave():
    data = request.get_json()
    employee_id = data['employee_id']
    leave_type = data.get('leave_type', 'Casual')
    start_date = data['start_date']
    end_date = data['end_date']
    reason = data.get('reason', '')

    sql = """
        INSERT INTO leaves (employee_id, leave_type, start_date, end_date, reason)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (employee_id, leave_type, start_date, end_date, reason))
    db.commit()
    return jsonify({"message": "Leave applied successfully"}), 201

# Get all leave requests (with employee name)
@app.route('/leaves', methods=['GET'])
def get_leaves():
    cursor.execute("""
        SELECT l.id, l.employee_id, e.name, l.leave_type, l.start_date, l.end_date,
               l.reason, l.status, l.applied_at
        FROM leaves l
        JOIN employees e ON l.employee_id = e.id
        ORDER BY l.applied_at DESC
    """)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "employee_id": row[1],
            "employee_name": row[2],
            "leave_type": row[3],
            "start_date": str(row[4]),
            "end_date": str(row[5]),
            "reason": row[6],
            "status": row[7],
            "applied_at": str(row[8])
        })
    return jsonify(result)

# Get leave history for one employee
@app.route('/leaves/<int:employee_id>', methods=['GET'])
def get_employee_leaves(employee_id):
    cursor.execute("""
        SELECT id, leave_type, start_date, end_date, reason, status, applied_at
        FROM leaves WHERE employee_id = %s ORDER BY applied_at DESC
    """, (employee_id,))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "leave_type": row[1],
            "start_date": str(row[2]),
            "end_date": str(row[3]),
            "reason": row[4],
            "status": row[5],
            "applied_at": str(row[6])
        })
    return jsonify(result)

# Approve or reject a leave request
@app.route('/leave/<int:leave_id>/status', methods=['PUT'])
def update_leave_status(leave_id):
    data = request.get_json()
    new_status = data['status']  # Approved or Rejected

    cursor.execute("UPDATE leaves SET status = %s WHERE id = %s", (new_status, leave_id))
    db.commit()
    return jsonify({"message": f"Leave {new_status.lower()} successfully"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
