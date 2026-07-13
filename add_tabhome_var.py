with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "const tabDashboard=document.getElementById('tabDashboard');"
new = old + "\n  const tabHome=document.getElementById('tabHome');"

if old in content:
    content = content.replace(old, new)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ tabHome variable added")
else:
    print("❌ Marker not found")
