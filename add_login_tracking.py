with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = """    session['user_id'] = user_id
    session['username'] = uname
    session['role'] = role
    session['employee_id'] = employee_id
    return jsonify({"username": uname, "role": role, "employee_id": employee_id}), 200"""

new = """    session['user_id'] = user_id
    session['username'] = uname
    session['role'] = role
    session['employee_id'] = employee_id
    cursor.execute("INSERT INTO login_activity (user_id, ip_address) VALUES (%s, %s)", (user_id, request.remote_addr))
    db.commit()
    return jsonify({"username": uname, "role": role, "employee_id": employee_id}), 200"""

if old in content:
    content = content.replace(old, new)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Login tracking added")
else:
    print("❌ Marker not found — checking exact match issue")
