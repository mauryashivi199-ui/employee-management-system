with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

js_code = '''
  document.getElementById('rowLoginActivity').addEventListener('click',()=>{
    fetch('/login-activity',{credentials:'include'}).then(r=>r.json()).then(rows=>{
      if(rows.length===0){alert('No login history yet.');return;}
      const msg = rows.map(r=>`${r.login_time} — IP: ${r.ip_address}`).join('\\n');
      alert('Recent Logins:\\n\\n' + msg);
    });
  });

  document.getElementById('rowMyAnalytics').addEventListener('click',()=>{
    fetch('/my-analytics',{credentials:'include'}).then(r=>r.json()).then(d=>{
      if(d.error){alert(d.error);return;}
      alert(`My Analytics (last ${d.total_days} days)\\n\\nAttendance: ${d.attendance_percentage}%\\nPresent: ${d.present}\\nHalf-day: ${d.half_day}\\nAbsent: ${d.absent}`);
    });
  });

  document.getElementById('rowAchievements').addEventListener('click',()=>{
    fetch('/my-achievements',{credentials:'include'}).then(r=>r.json()).then(d=>{
      if(d.error){alert(d.error);return;}
      let msg = `🔥 Current Streak: ${d.current_streak} days\\n⭐ Total Present: ${d.total_present} days\\n\\n`;
      if(d.badges.length===0){
        msg += 'No badges yet — keep showing up!';
      } else {
        msg += 'Badges Earned:\\n' + d.badges.map(b=>`${b.icon} ${b.name} — ${b.desc}`).join('\\n');
      }
      alert(msg);
    });
  });

  document.getElementById('rowExportData').addEventListener('click',()=>{
    fetch('/export-my-data',{credentials:'include'}).then(r=>r.json()).then(data=>{
      const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
      const url=URL.createObjectURL(blob);
      const a=document.createElement('a');
      a.href=url;a.download='my_ems_data.json';
      document.body.appendChild(a);a.click();a.remove();
      URL.revokeObjectURL(url);
      showToast('Data exported!','success');
    });
  });
'''

marker = "  checkSession();\n})();"
if marker in content:
    content = content.replace(marker, js_code + "\n  checkSession();\n})();")
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Unique features JS added")
else:
    print("❌ Marker not found")
