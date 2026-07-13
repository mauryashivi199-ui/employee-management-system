with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '<button class="nav-tab" id="tabDashboard" style="display:none;">Dashboard</button>'
new = old + '\n    <button class="nav-tab" id="tabSettings">Settings</button>'

if old in content:
    content = content.replace(old, new)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Settings tab button added")
else:
    print("❌ Marker not found")
