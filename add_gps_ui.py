with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

gps_card_html = '''<div class="card" id="gpsCheckinCard" style="display:none;background:var(--surface-alt);border:1px solid var(--border);border-radius:var(--radius-md);padding:16px;margin-bottom:16px;">
      <div style="display:flex;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:3px;margin-bottom:14px;">
        <div class="gps-mode-opt active" id="modeOffice" style="flex:1;text-align:center;padding:8px;border-radius:9px;font-size:12.5px;font-weight:700;cursor:pointer;">🏢 Office</div>
        <div class="gps-mode-opt" id="modeWFH" style="flex:1;text-align:center;padding:8px;border-radius:9px;font-size:12.5px;font-weight:700;cursor:pointer;color:var(--text-muted);">🏠 WFH</div>
      </div>
      <div id="gpsStatusBox" style="font-size:12.5px;color:var(--text-muted);margin-bottom:10px;">📍 Tap "Check In" to verify your location</div>
      <button class="btn btn-primary" id="gpsCheckinBtn" style="width:100%;justify-content:center;">✓ Check In</button>
    </div>
    <style>
      .gps-mode-opt.active{background:linear-gradient(135deg,var(--primary),#8B7CF6);color:#fff;}
    </style>
    '''

marker = '<div class="view" id="attendanceView">\n    <div class="att-header">'
new_marker = '<div class="view" id="attendanceView">\n    ' + gps_card_html + '<div class="att-header">'

if marker in content:
    content = content.replace(marker, new_marker)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ GPS card HTML added")
else:
    print("❌ Marker not found")
