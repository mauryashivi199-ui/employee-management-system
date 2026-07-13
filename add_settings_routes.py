with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

settings_routes = '''
@app.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user_id = session['user_id']
    emp_id = session.get('employee_id')
    cursor.execute("SELECT username, role FROM users WHERE id = %s", (user_id,))
    urow = cursor.fetchone()
    if not urow:
        return jsonify({"error": "User not found"}), 404
    result = {"username": urow[0], "role": urow[1], "employee_id": emp_id}
    if emp_id:
        cursor.execute("""
            SELECT e.name, e.email, e.department_id, d.name AS department_name
            FROM employees e LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.id = %s
        """, (emp_id,))
        erow = cursor.fetchone()
        if erow:
            result.update({"name": erow[0], "email": erow[1], "department_id": erow[2], "department": erow[3]})
    return jsonify(result)

@app.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    emp_id = session.get('employee_id')
    if not emp_id:
        return jsonify({"error": "No employee profile linked to this account"}), 400
    name = data.get('name')
    email = data.get('email')
    cursor.execute("UPDATE employees SET name = %s, email = %s WHERE id = %s", (name, email, emp_id))
    db.commit()
    if name:
        cursor.execute("UPDATE users SET username = username WHERE id = %s", (session['user_id'],))
    return jsonify({"message": "Profile updated successfully"}), 200

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    if not current_password or not new_password:
        return jsonify({"error": "Both current and new password required"}), 400
    if len(new_password) < 6:
        return jsonify({"error": "New password must be at least 6 characters"}), 400
    user_id = session['user_id']
    cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    if not row or not check_password_hash(row[0], current_password):
        return jsonify({"error": "Current password is incorrect"}), 401
    new_hash = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hash, user_id))
    db.commit()
    return jsonify({"message": "Password changed successfully"}), 200

'''

marker = "if __name__ == '__main__':"
if marker in content:
    content = content.replace(marker, settings_routes + marker)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Settings routes added")
else:
    print("❌ Marker not found")
