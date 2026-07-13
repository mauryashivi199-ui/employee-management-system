with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

home_html = '''  <div class="view active" id="homeView">
    <div style="background:linear-gradient(135deg,rgba(168,85,247,.15),rgba(6,182,212,.1));border:1px solid var(--border);border-radius:var(--radius-lg);padding:40px 32px;position:relative;overflow:hidden;margin-bottom:24px;">
      <div style="position:absolute;width:280px;height:280px;background:radial-gradient(circle,rgba(168,85,247,.25),transparent 70%);top:-100px;right:-60px;border-radius:50%;"></div>
      <div style="position:relative;z-index:1;max-width:640px;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
          <img src="/static/images/mcarbon_logo.jpg" alt="mCarbon" style="width:52px;height:52px;border-radius:50%;box-shadow:0 0 20px rgba(168,85,247,.4);">
          <span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent);background:rgba(6,182,212,.12);padding:4px 12px;border-radius:20px;">mCarbon Tech Innovation</span>
        </div>
        <h1 style="font-size:28px;margin:0 0 10px;background:linear-gradient(90deg,var(--primary-light),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Building Successful Customer Communication Journeys</h1>
        <p style="color:var(--text-muted);font-size:14.5px;line-height:1.6;margin:0;">Welcome to your Employee Management System — a single place to manage your team, track attendance, handle leave requests, and stay connected with everyone at mCarbon. We help businesses connect, communicate, and grow with reliable technology solutions.</p>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:24px;">
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:20px;text-align:center;">
        <div style="font-size:26px;">👥</div>
        <div id="homeStatEmployees" style="font-size:22px;font-weight:800;margin-top:6px;color:var(--primary-light);">--</div>
        <div style="font-size:11.5px;color:var(--text-muted);margin-top:2px;">Team Members</div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:20px;text-align:center;">
        <div style="font-size:26px;">🏢</div>
        <div id="homeStatDepts" style="font-size:22px;font-weight:800;margin-top:6px;color:var(--accent);">--</div>
        <div style="font-size:11.5px;color:var(--text-muted);margin-top:2px;">Departments</div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:20px;text-align:center;">
        <div style="font-size:26px;">✅</div>
        <div id="homeStatPresent" style="font-size:22px;font-weight:800;margin-top:6px;color:var(--success,#22c55e);">--</div>
        <div style="font-size:11.5px;color:var(--text-muted);margin-top:2px;">Present Today</div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:20px;text-align:center;">
        <div style="font-size:26px;">🌴</div>
        <div id="homeStatLeaves" style="font-size:22px;font-weight:800;margin-top:6px;color:var(--warning);">--</div>
        <div style="font-size:11.5px;color:var(--text-muted);margin-top:2px;">Pending Leaves</div>
      </div>
    </div>

    <p style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin:0 0 10px 4px;font-weight:700;">Quick Access</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;">
      <div class="home-quick-card" data-tab="employees" style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:20px;cursor:pointer;transition:.2s;">
        <div style="width:42px;height:42px;border-radius:12px;background:rgba(168,85,247,.15);display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:10px;">👤</div>
        <div style="font-weight:700;font-size:14px;">Employees</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:2px;">Manage team directory</div>
      </div>
      <div class="home-quick-card" data-tab="salary" style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:20px;cursor:pointer;transition:.2s;">
        <div style="width:42px;height:42px;border-radius:12px;background:rgba(6,182,212,.15);display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:10px;">💰</div>
        <div style="font-weight:700;font-size:14px;">Salary</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:2px;">View & manage payroll</div>
      </div>
      <div class="home-quick-card" data-tab="attendance" style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:20px;cursor:pointer;transition:.2s;">
        <div style="width:42px;height:42px;border-radius:12px;background:rgba(236,72,153,.15);display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:10px;">📍</div>
        <div style="font-weight:700;font-size:14px;">Attendance</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:2px;">GPS check-in & tracking</div>
      </div>
      <div class="home-quick-card" data-tab="leaves" style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:20px;cursor:pointer;transition:.2s;">
        <div style="width:42px;height:42px;border-radius:12px;background:rgba(251,191,36,.15);display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:10px;">🌴</div>
        <div style="font-weight:700;font-size:14px;">Leaves</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:2px;">Request & approve time off</div>
      </div>
    </div>
  </div>

  '''

marker = '  <div class="view" id="dashboardView">'
if marker in content:
    content = content.replace(marker, home_html + marker, 1)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Home view HTML added")
else:
    print("❌ Marker not found")
