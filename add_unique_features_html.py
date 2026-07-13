with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

marker = '<button id="settingsLogoutBtn"'

unique_html = '''<p style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin:22px 0 8px 4px;font-weight:700;">Unique Features</p>
        <div class="card" style="background:var(--surface-alt);border:1px solid var(--border);border-radius:var(--radius-md);overflow:hidden;">
          <div class="row" id="rowLoginActivity" style="display:flex;align-items:center;gap:12px;padding:13px 14px;border-bottom:1px solid var(--border);cursor:pointer;">
            <div style="width:34px;height:34px;border-radius:10px;background:rgba(168,85,247,.18);color:var(--primary-light);display:flex;align-items:center;justify-content:center;font-size:16px;">🕓</div>
            <div style="flex:1;"><div style="font-size:13.5px;font-weight:600;">Login Activity</div><div style="font-size:11px;color:var(--text-muted);">See recent sessions & devices</div></div>
            <div style="color:var(--text-muted);">›</div>
          </div>
          <div class="row" id="rowMyAnalytics" style="display:flex;align-items:center;gap:12px;padding:13px 14px;border-bottom:1px solid var(--border);cursor:pointer;">
            <div style="width:34px;height:34px;border-radius:10px;background:rgba(245,165,36,.18);color:var(--warning);display:flex;align-items:center;justify-content:center;font-size:16px;">📊</div>
            <div style="flex:1;"><div style="font-size:13.5px;font-weight:600;">My Analytics</div><div style="font-size:11px;color:var(--text-muted);">Personal attendance trends</div></div>
            <div style="color:var(--text-muted);">›</div>
          </div>
          <div class="row" id="rowAchievements" style="display:flex;align-items:center;gap:12px;padding:13px 14px;border-bottom:1px solid var(--border);cursor:pointer;">
            <div style="width:34px;height:34px;border-radius:10px;background:rgba(6,182,212,.18);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:16px;">🎯</div>
            <div style="flex:1;"><div style="font-size:13.5px;font-weight:600;">Goals & Achievements</div><div style="font-size:11px;color:var(--text-muted);">Streaks, badges, milestones</div></div>
            <div style="color:var(--text-muted);">›</div>
          </div>
          <div class="row" id="rowExportData" style="display:flex;align-items:center;gap:12px;padding:13px 14px;cursor:pointer;">
            <div style="width:34px;height:34px;border-radius:10px;background:rgba(18,184,134,.18);color:var(--accent-dark);display:flex;align-items:center;justify-content:center;font-size:16px;">📤</div>
            <div style="flex:1;"><div style="font-size:13.5px;font-weight:600;">Export My Data</div><div style="font-size:11px;color:var(--text-muted);">Download all your records (JSON)</div></div>
            <div style="color:var(--text-muted);">›</div>
          </div>
        </div>

        '''

if marker in content:
    content = content.replace(marker, unique_html + marker, 1)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Unique features HTML added")
else:
    print("❌ Marker not found")
