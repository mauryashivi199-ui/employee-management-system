with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "if(tab==='attendance'){tabAttendance.classList.add('active');attendanceView.classList.add('active');attActions.style.display='flex';loadAttendanceToday();}"
new = "if(tab==='attendance'){tabAttendance.classList.add('active');attendanceView.classList.add('active');attActions.style.display='flex';loadAttendanceToday();const gpsCard=document.getElementById('gpsCheckinCard');if(gpsCard){gpsCard.style.display=(currentUser&&currentUser.role==='employee')?'block':'none';}}"

if old in content:
    content = content.replace(old, new)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Visibility logic added")
else:
    print("❌ Pattern not found")
