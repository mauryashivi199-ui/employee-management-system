with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

settings_view_html = '''  <div class="view" id="settingsView">
    <div style="max-width:480px;">
      <div style="background:linear-gradient(90deg,var(--primary),var(--accent));border-radius:var(--radius-lg) var(--radius-lg) 0 0;padding:20px 20px 40px;position:relative;">
        <h2 style="margin:0;color:#fff;font-size:17px;">Settings</h2>
        <div style="position:absolute;bottom:-30px;left:20px;display:flex;align-items:center;gap:12px;">
          <div id="settingsAvatar" style="width:60px;height:60px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;color:var(--primary-dark);border:3px solid var(--surface);box-shadow:0 0 20px rgba(168,85,247,.5);">--</div>
        </div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-top:none;border-radius:0 0 var(--radius-lg) var(--radius-lg);padding:44px 20px 24px;">
        <div>
          <h3 id="settingsName" style="margin:0;font-size:16px;">--</h3>
          <span id="settingsEmail" style="font-size:12px;color:var(--text-muted);">--</span><br>
          <span id="settingsRole" class="role-tag" style="margin-top:6px;display:inline-block;">--</span>
        </div>

        <div id="settingsSalaryBlock" style="display:none;margin-top:20px;">
          <p style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin:0 0 8px 4px;font-weight:700;">Salary</p>
          <div style="background:linear-gradient(135deg,rgba(168,85,247,.12),rgba(6,182,212,.08));border:1px solid var(--border);border-radius:var(--radius-md);padding:16px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
              <div><div style="font-size:11px;color:var(--text-muted);">Net Salary</div><div id="settingsNetSalary" style="font-size:22px;font-weight:800;color:var(--primary);">--</div></div>
              <div id="settingsSalaryMonth" style="font-size:10.5px;background:var(--surface-alt);padding:3px 9px;border-radius:20px;color:var(--text-muted);">--</div>
            </div>
            <div style="display:flex;gap:16px;margin-top:14px;">
              <div style="flex:1;"><div style="font-size:10px;color:var(--text-muted);">Basic</div><div id="settingsBasic" style="font-size:13px;font-weight:700;">--</div></div>
              <div style="flex:1;"><div style="font-size:10px;color:var(--text-muted);">HRA + Allow.</div><div id="settingsAllowance" style="font-size:13px;font-weight:700;color:var(--accent);">--</div></div>
              <div style="flex:1;"><div style="font-size:10px;color:var(--text-muted);">Deductions</div><div id="settingsDeductions" style="font-size:13px;font-weight:700;color:var(--danger);">--</div></div>
            </div>
          </div>
        </div>

        <p style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin:22px 0 8px 4px;font-weight:700;">Account</p>
        <div class="card" style="background:var(--surface-alt);border:1px solid var(--border);border-radius:var(--radius-md);overflow:hidden;">
          <div class="row" id="rowEditProfile" style="display:flex;align-items:center;gap:12px;padding:13px 14px;border-bottom:1px solid var(--border);cursor:pointer;">
            <div style="width:34px;height:34px;border-radius:10px;background:rgba(168,85,247,.18);color:var(--primary-light);display:flex;align-items:center;justify-content:center;font-size:16px;">👤</div>
            <div style="flex:1;"><div style="font-size:13.5px;font-weight:600;">Edit Profile</div><div style="font-size:11px;color:var(--text-muted);">Name, email</div></div>
            <div style="color:var(--text-muted);">›</div>
          </div>
          <div class="row" id="rowChangePassword" style="display:flex;align-items:center;gap:12px;padding:13px 14px;cursor:pointer;">
            <div style="width:34px;height:34px;border-radius:10px;background:rgba(6,182,212,.18);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:16px;">🔒</div>
            <div style="flex:1;"><div style="font-size:13.5px;font-weight:600;">Change Password</div><div style="font-size:11px;color:var(--text-muted);">Update login credentials</div></div>
            <div style="color:var(--text-muted);">›</div>
          </div>
        </div>

        <button id="settingsLogoutBtn" style="margin-top:22px;width:100%;padding:12px;border-radius:12px;border:1px solid rgba(239,71,111,.35);background:rgba(239,71,111,.08);color:var(--danger);font-weight:700;font-size:13px;cursor:pointer;">🚪 Log Out</button>
      </div>
    </div>
  </div>
'''

marker = '  <div class="view" id="dashboardView">'
if marker in content:
    content = content.replace(marker, settings_view_html + marker, 1)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Settings view HTML added")
else:
    print("❌ Marker not found")
