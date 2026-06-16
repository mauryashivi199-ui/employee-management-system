from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

employees = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/employee', methods=['POST'])
def add_employee():
    data = request.get_json()

    employee = {
        "id": data["id"],
        "name": data["name"],
        "department": data["department"]
    }

    employees.append(employee)

    return jsonify({
        "message": "Employee Added Successfully",
        "employee": employee
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)