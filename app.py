from flask import Flask, request, jsonify, render_template, session
import mysql.connector
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__, template_folder='templates')
app.secret_key = 'change-this-secret-key-in-production'

db = mysql.connector.connect(
    host="mysql-service",
    user="root",
    password="root",
    database="mydb"
)
cursor = db.cursor()

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Login required"}), 401
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Login required"}), 401
        if session.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return wrapper

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cursor.execute("SELECT id, username, password, role, employee_id FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()

    if not row:
        return jsonify({"error": "Invalid username or password"}), 401

    user_id, uname, stored_password, role, employee_id = row

    valid = False
    if stored_password.startswith('pbkdf2:') or stored_password.startswith('scrypt:'):
        valid = check_password_hash(stored_password, password)
    else:
        valid = (stored_password == password)

    if not valid:
        return jsonify({"error": "Invalid username or password"}), 401

    session['user_id'] = user_id
    session['username'] = uname
    session['role'] = role
    session['employee_id'] = employee_id

    return jsonify({"username": uname, "role": role, "employee_id": employee_id}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

@app.route('/me', methods=['GET'])
def me():
    if 'user_id' not in session:
        return jsonify({"logged_in": False}), 200
    return jsonify({
        "logged_in": True,
        "username": session.get('username'),
        "role": session.get('role'),
        "employee_id": session.get('employee_id')
    }), 200

@app.route('/employee', methods=['POST'])
@admin_required
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
@login_required
def get_employees():
    role = session.get('role')
    emp_id = session.get('employee_id')

    if role == 'employee' and emp_id:
        cursor.execute("""
            SELECT e.id, e.name, e.email, e.department_id, d.name AS department_name
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.id = %s
        """, (emp_id,))
    else:
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
@login_required
def get_departments():
    cursor.execute("SELECT id, name FROM departments")
    rows = cursor.fetchall()
    result = [{"id": row[0], "name": row[1]} for row in rows]
    return jsonify(result)

@app.route('/attendance', methods=['POST'])
@admin_required
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
@login_required
def get_attendance():
    role = session.get('role')
    emp_id = session.get('employee_id')

    if role == 'employee' and emp_id:
        cursor.execute("""
            SELECT a.id, a.employee_id, e.name, a.date, a.status
            FROM attendance a
            JOIN employees e ON a.employee_id = e.id
            WHERE a.employee_id = %s
            ORDER BY a.date DESC
        """, (emp_id,))
    else:
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
@login_required
def get_employee_attendance(employee_id):
    role = session.get('role')
    emp_id = session.get('employee_id')

    if role == 'employee' and emp_id != employee_id:
        return jsonify({"error": "Access denied"}), 403

    cursor.execute("""
        SELECT id, date, status FROM attendance
        WHERE employee_id = %s ORDER BY date DESC
    """, (employee_id,))
    rows = cursor.fetchall()
    result = [{"id": row[0], "date": str(row[1]), "status": row[2]} for row in rows]
    return jsonify(result)

@app.route('/attendance/today', methods=['GET'])
@login_required
def get_today_attendance():
    role = session.get('role')
    emp_id = session.get('employee_id')
    today = str(date.today())

    if role == 'employee' and emp_id:
        cursor.execute("""
            SELECT e.id, e.name, a.status
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id AND a.date = %s
            WHERE e.id = %s
        """, (today, emp_id))
    else:
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

@app.route('/leave', methods=['POST'])
@login_required
def apply_leave():
    data = request.get_json()
    role = session.get('role')
    session_emp_id = session.get('employee_id')

    employee_id = data['employee_id']
    # Employees can only apply leave for themselves
    if role == 'employee' and session_emp_id != employee_id:
        return jsonify({"error": "You can only apply leave for yourself"}), 403

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

@app.route('/leaves', methods=['GET'])
@login_required
def get_leaves():
    role = session.get('role')
    emp_id = session.get('employee_id')

    if role == 'employee' and emp_id:
        cursor.execute("""
            SELECT l.id, l.employee_id, e.name, l.leave_type, l.start_date, l.end_date,
                   l.reason, l.status, l.applied_at
            FROM leaves l
            JOIN employees e ON l.employee_id = e.id
            WHERE l.employee_id = %s
            ORDER BY l.applied_at DESC
        """, (emp_id,))
    else:
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

@app.route('/leaves/<int:employee_id>', methods=['GET'])
@login_required
def get_employee_leaves(employee_id):
    role = session.get('role')
    emp_id = session.get('employee_id')

    if role == 'employee' and emp_id != employee_id:
        return jsonify({"error": "Access denied"}), 403

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

@app.route('/leave/<int:leave_id>/status', methods=['PUT'])
@admin_required
def update_leave_status(leave_id):
    data = request.get_json()
    new_status = data['status']

    cursor.execute("UPDATE leaves SET status = %s WHERE id = %s", (new_status, leave_id))
    db.commit()
    return jsonify({"message": f"Leave {new_status.lower()} successfully"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
