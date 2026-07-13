with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = """  function switchTab(tab){
    [tabEmployees,tabAttendance,tabLeaves,tabSalary,tabDashboard].forEach(t=>t.classList.remove('active'));
    [employeesView,attendanceView,leavesView,salaryView,dashboardView,document.getElementById('settingsView')].forEach(v=>v.classList.remove('active'));
    employeesActions.style.display='none';leavesActions.style.display='none';
    attActions.style.display='none';dashActions.style.display='none';salaryActions.style.display='none';
    if(tab==='employees'){tabEmployees.classList.add('active');employeesView.classList.add('active');employeesActions.style.display='flex';}
    if(tab==='attendance'){tabAttendance.classList.add('active');attendanceView.classList.add('active');attActions.style.display='flex';loadAttendanceToday();const gpsCard=document.getElementById('gpsCheckinCard');if(gpsCard){gpsCard.style.display=(currentUser&&currentUser.role==='employee')?'block':'none';}}
    if(tab==='leaves'){tabLeaves.classList.add('active');leavesView.classList.add('active');leavesActions.style.display='flex';loadLeaves();}
    if(tab==='salary'){tabSalary.classList.add('active');salaryView.classList.add('active');salaryActions.style.display='flex';loadSalaries();}
    if(tab==='dashboard'){tabDashboard.classList.add('active');dashboardView.classList.add('active');dashActions.style.display='flex';loadDashboard();}
    if(tab==='settings'){tabSettings.classList.add('active');document.getElementById('settingsView').classList.add('active');loadSettingsProfile();}
  }"""

new = """  function switchTab(tab){
    [tabHome,tabEmployees,tabAttendance,tabLeaves,tabSalary,tabDashboard].forEach(t=>t.classList.remove('active'));
    [document.getElementById('homeView'),employeesView,attendanceView,leavesView,salaryView,dashboardView,document.getElementById('settingsView')].forEach(v=>v.classList.remove('active'));
    employeesActions.style.display='none';leavesActions.style.display='none';
    attActions.style.display='none';dashActions.style.display='none';salaryActions.style.display='none';
    if(tab==='home'){tabHome.classList.add('active');document.getElementById('homeView').classList.add('active');loadHomeStats();}
    if(tab==='employees'){tabEmployees.classList.add('active');employeesView.classList.add('active');employeesActions.style.display='flex';}
    if(tab==='attendance'){tabAttendance.classList.add('active');attendanceView.classList.add('active');attActions.style.display='flex';loadAttendanceToday();const gpsCard=document.getElementById('gpsCheckinCard');if(gpsCard){gpsCard.style.display=(currentUser&&currentUser.role==='employee')?'block':'none';}}
    if(tab==='leaves'){tabLeaves.classList.add('active');leavesView.classList.add('active');leavesActions.style.display='flex';loadLeaves();}
    if(tab==='salary'){tabSalary.classList.add('active');salaryView.classList.add('active');salaryActions.style.display='flex';loadSalaries();}
    if(tab==='dashboard'){tabDashboard.classList.add('active');dashboardView.classList.add('active');dashActions.style.display='flex';loadDashboard();}
    if(tab==='settings'){document.getElementById('settingsView').classList.add('active');loadSettingsProfile();}
  }

  function loadHomeStats(){
    fetch('/employees',{credentials:'include'}).then(r=>r.json()).then(emps=>{
      document.getElementById('homeStatEmployees').textContent=emps.length;
      const depts=new Set(emps.map(e=>e.department_id)).size;
      document.getElementById('homeStatDepts').textContent=depts;
    });
    fetch('/attendance/today',{credentials:'include'}).then(r=>r.json()).then(data=>{
      const present=data.filter(a=>a.status==='Present').length;
      document.getElementById('homeStatPresent').textContent=present;
    });
    fetch('/leaves',{credentials:'include'}).then(r=>r.json()).then(data=>{
      const pending=data.filter(l=>l.status==='Pending').length;
      document.getElementById('homeStatLeaves').textContent=pending;
    });
  }

  document.querySelectorAll('.home-quick-card').forEach(card=>{
    card.addEventListener('click',()=>switchTab(card.dataset.tab));
  });"""

if old in content:
    content = content.replace(old, new)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ switchTab updated with Home logic")
else:
    print("❌ Marker not found")
