with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

js_code = '''
  const dotMenuBtn=document.getElementById('dotMenuBtn');
  const dotMenuDropdown=document.getElementById('dotMenuDropdown');
  if(dotMenuBtn){
    dotMenuBtn.addEventListener('click',(e)=>{
      e.stopPropagation();
      dotMenuDropdown.hidden=!dotMenuDropdown.hidden;
    });
    document.addEventListener('click',()=>{dotMenuDropdown.hidden=true;});
    document.querySelectorAll('.dot-menu-item').forEach(item=>{
      item.addEventListener('click',()=>{
        const action=item.dataset.action;
        dotMenuDropdown.hidden=true;
        if(action==='settings'){switchTab('settings');}
        if(action==='logout'){fetch('/logout',{method:'POST',credentials:'include'}).then(()=>location.reload());}
        if(action==='help'){alert('Help & Support\\n\\nFor assistance, contact HR at hr@mcarbontech.com\\n\\nFAQs:\\n- How do I mark attendance? Go to Attendance tab, use GPS check-in.\\n- How do I apply for leave? Go to Leaves tab and submit a request.\\n- Forgot password? Contact your admin.');}
        if(action==='about'){alert('About EMS\\n\\nEmployee Management System v2.0\\nBuilt for mCarbon Tech Innovation\\n\\nFeatures: Attendance, Leave Management, Salary, Real-time Chat, GPS Check-in');}
      });
    });
  }
'''

marker = "  checkSession();\n})();"
if marker in content:
    content = content.replace(marker, js_code + "\n  checkSession();\n})();")
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Dot menu JS added")
else:
    print("❌ Marker not found")
