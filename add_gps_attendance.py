with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

gps_code = '''
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

'''

marker = "if __name__ == '__main__':"
if marker in content:
    content = content.replace(marker, gps_code + marker)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ GPS attendance route added")
else:
    print("❌ Marker not found")
