with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

chat_routes = '''
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

'''

marker = "if __name__ == '__main__':"
if marker in content:
    content = content.replace(marker, chat_routes + marker)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Chat routes added successfully")
else:
    print("❌ Marker not found, kuch galat hai")
