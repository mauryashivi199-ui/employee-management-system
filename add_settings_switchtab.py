with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "if(tab==='dashboard'){tabDashboard.classList.add('active');dashboardView.classList.add('active');dashActions.style.display='flex';loadDashboard();}"
new = old + "\n    if(tab==='settings'){tabSettings.classList.add('active');document.getElementById('settingsView').classList.add('active');loadSettingsProfile();}"

if old in content:
    content = content.replace(old, new)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ switchTab settings case added")
else:
    print("❌ old marker not found")
