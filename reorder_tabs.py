with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_tabs = '''<div class="nav-tabs">
    <button class="nav-tab active" id="tabEmployees">Employees</button>
    <button class="nav-tab" id="tabAttendance">Attendance</button>
    <button class="nav-tab" id="tabLeaves">Leaves</button>
    <button class="nav-tab" id="tabSalary">Salary</button>
    <button class="nav-tab" id="tabDashboard" style="display:none;">Dashboard</button>
    <button class="nav-tab" id="tabSettings">Settings</button>'''

new_tabs = '''<div class="nav-tabs">
    <button class="nav-tab active" id="tabHome">Home</button>
    <button class="nav-tab" id="tabDashboard" style="display:none;">Dashboard</button>
    <button class="nav-tab" id="tabEmployees">Employees</button>
    <button class="nav-tab" id="tabSalary">Salary</button>
    <button class="nav-tab" id="tabAttendance">Attendance</button>
    <button class="nav-tab" id="tabLeaves">Leaves</button>'''

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Tabs reordered, Home added, Settings tab removed")
else:
    print("❌ Marker not found")
