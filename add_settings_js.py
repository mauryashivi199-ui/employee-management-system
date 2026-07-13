with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "tabDashboard.addEventListener('click',()=>switchTab('dashboard'));"
new = old + "\n  tabSettings.addEventListener('click',()=>switchTab('settings'));"

if old in content:
    content = content.replace(old, new)
else:
    print("❌ listener marker not found")

settings_logic = '''
  function loadSettingsProfile(){
    fetch('/profile',{credentials:'include'}).then(r=>r.json()).then(p=>{
      document.getElementById('settingsAvatar').textContent=(p.name||p.username||'?').charAt(0).toUpperCase();
      document.getElementById('settingsName').textContent=p.name||p.username;
      document.getElementById('settingsEmail').textContent=p.email||p.username;
      document.getElementById('settingsRole').textContent=p.role;
      const salaryBlock=document.getElementById('settingsSalaryBlock');
      if(p.role==='employee'&&p.employee_id){
        salaryBlock.style.display='block';
        fetch(`/salary/${p.employee_id}`,{credentials:'include'}).then(r=>r.json()).then(rows=>{
          if(rows&&rows.length>0){
            const s=rows[0];
            document.getElementById('settingsNetSalary').textContent='₹'+Number(s.net_salary).toLocaleString('en-IN');
            document.getElementById('settingsBasic').textContent='₹'+Number(s.basic_salary).toLocaleString('en-IN');
            document.getElementById('settingsAllowance').textContent='+₹'+(Number(s.hra)+Number(s.other_allowances)).toLocaleString('en-IN');
            document.getElementById('settingsDeductions').textContent='−₹'+Number(s.deductions).toLocaleString('en-IN');
            document.getElementById('settingsSalaryMonth').textContent=s.effective_month;
          } else {
            document.getElementById('settingsNetSalary').textContent='Not set';
          }
        });
      } else {
        salaryBlock.style.display='none';
      }
    });
  }

  document.getElementById('rowEditProfile').addEventListener('click',()=>{
    const newName=prompt('Enter new name:');
    if(newName===null||!newName.trim())return;
    const newEmail=prompt('Enter new email:');
    if(newEmail===null||!newEmail.trim())return;
    fetch('/profile',{
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      credentials:'include',
      body:JSON.stringify({name:newName.trim(),email:newEmail.trim()})
    }).then(r=>r.json().then(d=>({status:r.status,d})))
    .then(({status,d})=>{
      if(status===200){showToast('Profile updated!','success');loadSettingsProfile();}
      else{showToast(d.error||'Update failed','danger');}
    });
  });

  document.getElementById('rowChangePassword').addEventListener('click',()=>{
    const current=prompt('Enter current password:');
    if(current===null)return;
    const newPass=prompt('Enter new password (min 6 characters):');
    if(newPass===null)return;
    fetch('/change-password',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      credentials:'include',
      body:JSON.stringify({current_password:current,new_password:newPass})
    }).then(r=>r.json().then(d=>({status:r.status,d})))
    .then(({status,d})=>{
      if(status===200){showToast('Password changed successfully!','success');}
      else{showToast(d.error||'Change failed','danger');}
    });
  });

  document.getElementById('settingsLogoutBtn').addEventListener('click',()=>{
    fetch('/logout',{method:'POST',credentials:'include'}).then(()=>{location.reload();});
  });
'''

marker = "  checkSession();\n})();"
if marker in content:
    content = content.replace(marker, settings_logic + "\n  checkSession();\n})();")
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Settings JS logic added")
else:
    print("❌ checkSession marker not found")
