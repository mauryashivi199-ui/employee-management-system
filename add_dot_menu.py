with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

dot_menu_html = '''<div style="position:relative;margin-left:6px;">
      <button id="dotMenuBtn" style="width:34px;height:34px;border-radius:10px;border:1px solid var(--border);background:var(--surface-alt);color:var(--text);font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;">⋮</button>
      <div id="dotMenuDropdown" hidden style="position:absolute;top:42px;right:0;background:var(--surface);border:1px solid var(--border);border-radius:12px;box-shadow:0 20px 50px rgba(168,85,247,.2);min-width:200px;z-index:50;overflow:hidden;">
        <div class="dot-menu-item" data-action="settings" style="padding:12px 16px;font-size:13px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--border);">⚙️ Settings</div>
        <div class="dot-menu-item" data-action="help" style="padding:12px 16px;font-size:13px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--border);">❓ Help & Support</div>
        <div class="dot-menu-item" data-action="about" style="padding:12px 16px;font-size:13px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--border);">ℹ️ About EMS</div>
        <div class="dot-menu-item" data-action="logout" style="padding:12px 16px;font-size:13px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:10px;color:var(--danger);">🚪 Log Out</div>
      </div>
    </div>
  </header>'''

old = "  </header>"
if old in content:
    content = content.replace(old, dot_menu_html, 1)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Dot menu HTML added")
else:
    print("❌ Marker not found")
