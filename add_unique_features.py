with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

unique_features_code = '''
@app.route('/login-activity', methods=['GET'])
@login_required
def login_activity():
    user_id = session['user_id']
    cursor.execute("""
        SELECT login_time, ip_address FROM login_activity
        WHERE user_id = %s ORDER BY login_time DESC LIMIT 10
    """, (user_id,))
    rows = cursor.fetchall()
    result = [{"login_time": r[0].strftime('%d %b %Y, %I:%M %p'), "ip_address": r[1] or "Unknown"} for r in rows]
    return jsonify(result)

@app.route('/my-analytics', methods=['GET'])
@login_required
def my_analytics():
    emp_id = session.get('employee_id')
    if not emp_id:
        return jsonify({"error": "No employee profile"}), 400
    cursor.execute("""
        SELECT date, status FROM attendance
        WHERE employee_id = %s ORDER BY date DESC LIMIT 30
    """, (emp_id,))
    rows = cursor.fetchall()
    total = len(rows)
    present = sum(1 for r in rows if r[1] == 'Present')
    half = sum(1 for r in rows if r[1] == 'Half-day')
    absent = sum(1 for r in rows if r[1] == 'Absent')
    percentage = round(((present + 0.5*half) / total) * 100, 1) if total > 0 else 0
    trend = [{"date": r[0].strftime('%d %b'), "status": r[1]} for r in reversed(rows)]
    return jsonify({
        "total_days": total, "present": present, "half_day": half, "absent": absent,
        "attendance_percentage": percentage, "trend": trend
    })

@app.route('/my-achievements', methods=['GET'])
@login_required
def my_achievements():
    emp_id = session.get('employee_id')
    if not emp_id:
        return jsonify({"error": "No employee profile"}), 400
    cursor.execute("""
        SELECT date, status FROM attendance
        WHERE employee_id = %s ORDER BY date DESC
    """, (emp_id,))
    rows = cursor.fetchall()
    streak = 0
    for r in rows:
        if r[1] in ('Present', 'Half-day'):
            streak += 1
        else:
            break
    total_present = sum(1 for r in rows if r[1] == 'Present')
    badges = []
    if streak >= 7: badges.append({"name": "Week Warrior", "icon": "🔥", "desc": "7+ day streak"})
    if streak >= 30: badges.append({"name": "Monthly Master", "icon": "🏆", "desc": "30+ day streak"})
    if total_present >= 50: badges.append({"name": "Consistency King/Queen", "icon": "⭐", "desc": "50+ days present"})
    if total_present >= 100: badges.append({"name": "Century Club", "icon": "💯", "desc": "100+ days present"})
    return jsonify({"current_streak": streak, "total_present": total_present, "badges": badges})

@app.route('/export-my-data', methods=['GET'])
@login_required
def export_my_data():
    emp_id = session.get('employee_id')
    user_id = session['user_id']
    data = {"exported_at": str(date.today())}

    cursor.execute("SELECT username, role FROM users WHERE id = %s", (user_id,))
    urow = cursor.fetchone()
    data["account"] = {"username": urow[0], "role": urow[1]} if urow else {}

    if emp_id:
        cursor.execute("SELECT name, email FROM employees WHERE id = %s", (emp_id,))
        erow = cursor.fetchone()
        data["profile"] = {"name": erow[0], "email": erow[1]} if erow else {}

        cursor.execute("SELECT date, status, location_type FROM attendance WHERE employee_id = %s ORDER BY date DESC", (emp_id,))
        data["attendance"] = [{"date": str(r[0]), "status": r[1], "location_type": r[2]} for r in cursor.fetchall()]

        cursor.execute("SELECT leave_type, start_date, end_date, status FROM leaves WHERE employee_id = %s", (emp_id,))
        data["leaves"] = [{"type": r[0], "start": str(r[1]), "end": str(r[2]), "status": r[3]} for r in cursor.fetchall()]

    return jsonify(data)

'''

marker = "if __name__ == '__main__':"
if marker in content:
    content = content.replace(marker, unique_features_code + marker)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Unique features routes added")
else:
    print("❌ Marker not found")
