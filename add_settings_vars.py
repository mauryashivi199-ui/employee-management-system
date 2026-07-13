with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old1 = "const tabDashboard=document.getElementById('tabDashboard');"
new1 = old1 + "\n  const tabSettings=document.getElementById('tabSettings');"

old2 = "[employeesView,attendanceView,leavesView,salaryView,dashboardView].forEach(v=>v.classList.remove('active'));"
new2 = "[employeesView,attendanceView,leavesView,salaryView,dashboardView,document.getElementById('settingsView')].forEach(v=>v.classList.remove('active'));"

count = 0
if old1 in content:
    content = content.replace(old1, new1)
    count += 1
if old2 in content:
    content = content.replace(old2, new2)
    count += 1

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ Applied {count}/2 patches")
