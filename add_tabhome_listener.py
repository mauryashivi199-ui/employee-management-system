with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "tabDashboard.addEventListener('click',()=>switchTab('dashboard'));"
new = old + "\n  tabHome.addEventListener('click',()=>switchTab('home'));"

if old in content:
    content = content.replace(old, new)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ tabHome listener added")
else:
    print("❌ Marker not found")
