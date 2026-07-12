from flask import Flask, request, jsonify, render_template, session
import mysql.connector
from datetime import date, timedelta
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

@app.route('/dashboard/stats', methods=['GET'])
@admin_required
def dashboard_stats():
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]

    today = date.today()
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = %s AND status = 'Present'", (today,))
    present_today = cursor.fetchone()[0]
    present_pct = round((present_today / total_employees) * 100) if total_employees else 0

    cursor.execute("SELECT COUNT(*) FROM leaves WHERE status = 'Pending'")
    pending_leaves = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM leaves
        WHERE status = 'Approved' AND MONTH(applied_at) = MONTH(CURDATE()) AND YEAR(applied_at) = YEAR(CURDATE())
    """)
    approved_this_month = cursor.fetchone()[0]

    trend = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = %s AND status = 'Present'", (d,))
        present_count = cursor.fetchone()[0]
        pct = round((present_count / total_employees) * 100) if total_employees else 0
        trend.append({"date": str(d), "day": d.strftime('%a'), "percent": pct})

    cursor.execute("""
        SELECT leave_type, COUNT(*) FROM leaves
        WHERE MONTH(start_date) = MONTH(CURDATE()) AND YEAR(start_date) = YEAR(CURDATE())
        GROUP BY leave_type
    """)
    leave_rows = cursor.fetchall()
    leave_by_type = {row[0]: row[1] for row in leave_rows}
    for lt in ['Sick', 'Casual', 'Paid']:
        leave_by_type.setdefault(lt, 0)

    cursor.execute("""
        SELECT d.name, COUNT(e.id) FROM departments d
        LEFT JOIN employees e ON e.department_id = d.id
        GROUP BY d.id, d.name
    """)
    dept_rows = cursor.fetchall()
    dept_breakdown = [{"department": row[0], "count": row[1]} for row in dept_rows]

    return jsonify({
        "total_employees": total_employees,
        "present_today_pct": present_pct,
        "pending_leaves": pending_leaves,
        "approved_this_month": approved_this_month,
        "attendance_trend": trend,
        "leave_by_type": leave_by_type,
        "dept_breakdown": dept_breakdown
    })

# ---------- Salary ----------
@app.route('/salary', methods=['POST'])
@admin_required
def set_salary():
    data = request.get_json()
    employee_id = data['employee_id']
    basic_salary = float(data.get('basic_salary', 0))
    hra = float(data.get('hra', 0))
    other_allowances = float(data.get('other_allowances', 0))
    deductions = float(data.get('deductions', 0))
    effective_month = data['effective_month']  # format: "2026-07"

    net_salary = basic_salary + hra + other_allowances - deductions

    sql = """
        INSERT INTO salary (employee_id, basic_salary, hra, other_allowances, deductions, net_salary, effective_month)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            basic_salary = VALUES(basic_salary),
            hra = VALUES(hra),
            other_allowances = VALUES(other_allowances),
            deductions = VALUES(deductions),
            net_salary = VALUES(net_salary)
    """
    cursor.execute(sql, (employee_id, basic_salary, hra, other_allowances, deductions, net_salary, effective_month))
    db.commit()
    return jsonify({"message": "Salary saved successfully", "net_salary": net_salary}), 201

@app.route('/salary', methods=['GET'])
@admin_required
def get_all_salaries():
    cursor.execute("""
        SELECT s.id, s.employee_id, e.name, s.basic_salary, s.hra, s.other_allowances,
               s.deductions, s.net_salary, s.effective_month
        FROM salary s
        JOIN employees e ON s.employee_id = e.id
        ORDER BY s.effective_month DESC, e.name
    """)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "employee_id": row[1],
            "employee_name": row[2],
            "basic_salary": float(row[3]),
            "hra": float(row[4]),
            "other_allowances": float(row[5]),
            "deductions": float(row[6]),
            "net_salary": float(row[7]),
            "effective_month": row[8]
        })
    return jsonify(result)

@app.route('/salary/<int:employee_id>', methods=['GET'])
@login_required
def get_employee_salary(employee_id):
    role = session.get('role')
    emp_id = session.get('employee_id')

    if role == 'employee' and emp_id != employee_id:
        return jsonify({"error": "Access denied"}), 403

    cursor.execute("""
        SELECT id, basic_salary, hra, other_allowances, deductions, net_salary, effective_month
        FROM salary WHERE employee_id = %s ORDER BY effective_month DESC
    """, (employee_id,))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "basic_salary": float(row[1]),
            "hra": float(row[2]),
            "other_allowances": float(row[3]),
            "deductions": float(row[4]),
            "net_salary": float(row[5]),
            "effective_month": row[6]
        })
    return jsonify(result)


@app.route('/chat/contacts', methods=['GET'])
@login_required
def chat_contacts():
    role = session.get('role')
    if role == 'admin':
        cursor.execute("SELECT id, username, role FROM users WHERE role = 'employee'")
    else:
        cursor.execute("SELECT id, username, role FROM users WHERE role = 'admin'")
    rows = cursor.fetchall()
    result = [{"id": r[0], "username": r[1], "role": r[2]} for r in rows]
    return jsonify(result)

@app.route('/chat/history/<int:other_user_id>', methods=['GET'])
@login_required
def chat_history(other_user_id):
    current_id = session['user_id']
    cursor.execute("""
        SELECT id, sender_id, receiver_id, message, timestamp
        FROM chat_messages
        WHERE (sender_id = %s AND receiver_id = %s)
           OR (sender_id = %s AND receiver_id = %s)
        ORDER BY timestamp ASC
    """, (current_id, other_user_id, other_user_id, current_id))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "sender_id": row[1],
            "receiver_id": row[2],
            "message": row[3],
            "timestamp": row[4].strftime('%H:%M')
        })
    cursor.execute("""
        UPDATE chat_messages SET is_read = TRUE
        WHERE sender_id = %s AND receiver_id = %s AND is_read = FALSE
    """, (other_user_id, current_id))
    db.commit()
    return jsonify(result)

@app.route('/chat/send', methods=['POST'])
@login_required
def chat_send():
    data = request.get_json()
    sender_id = session['user_id']
    receiver_id = data['receiver_id']
    message = data['message'].strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400
    cursor.execute("""
        INSERT INTO chat_messages (sender_id, receiver_id, message)
        VALUES (%s, %s, %s)
    """, (sender_id, receiver_id, message))
    db.commit()
    return jsonify({"message": "sent"}), 201

@app.route('/chat/unread-count', methods=['GET'])
@login_required
def chat_unread_count():
    current_id = session['user_id']
    cursor.execute("""
        SELECT COUNT(*) FROM chat_messages
        WHERE receiver_id = %s AND is_read = FALSE
    """, (current_id,))
    count = cursor.fetchone()[0]
    return jsonify({"unread": count})


import math

OFFICE_LAT = 28.5154
OFFICE_LNG = 77.3767
GEOFENCE_RADIUS_METERS = 150

def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.route('/attendance/checkin', methods=['POST'])
@login_required
def attendance_checkin():
    data = request.get_json()
    emp_id = session.get('employee_id')
    location_type = data.get('location_type', 'office')
    lat = data.get('latitude')
    lng = data.get('longitude')
    today = date.today()

    distance = None
    if location_type == 'office':
        if lat is None or lng is None:
            return jsonify({"error": "Location access required for office check-in"}), 400
        distance = calculate_distance(float(lat), float(lng), OFFICE_LAT, OFFICE_LNG)
        if distance > GEOFENCE_RADIUS_METERS:
            return jsonify({
                "error": f"You are {int(distance)}m away from office. Must be within {GEOFENCE_RADIUS_METERS}m to check in.",
                "distance": int(distance)
            }), 403

    cursor.execute("SELECT id FROM attendance WHERE employee_id = %s AND date = %s", (emp_id, today))
    existing = cursor.fetchone()
    if existing:
        return jsonify({"error": "Already checked in today"}), 400

    cursor.execute("""
        INSERT INTO attendance (employee_id, date, status, location_type, latitude, longitude, distance_meters)
        VALUES (%s, %s, 'Present', %s, %s, %s, %s)
    """, (emp_id, today, location_type, lat, lng, int(distance) if distance else None))
    db.commit()

    return jsonify({
        "message": "Checked in successfully",
        "location_type": location_type,
        "distance": int(distance) if distance else None
    }), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
