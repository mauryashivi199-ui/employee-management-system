with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

gps_js = '''
  let gpsMode = 'office';
  const modeOfficeBtn = document.getElementById('modeOffice');
  const modeWFHBtn = document.getElementById('modeWFH');
  const gpsStatusBox = document.getElementById('gpsStatusBox');
  const gpsCheckinBtn = document.getElementById('gpsCheckinBtn');
  const gpsCheckinCard = document.getElementById('gpsCheckinCard');

  if(modeOfficeBtn){
    modeOfficeBtn.addEventListener('click', () => {
      gpsMode = 'office';
      modeOfficeBtn.classList.add('active');
      modeWFHBtn.classList.remove('active');
      gpsStatusBox.textContent = '📍 Tap "Check In" to verify your location';
    });
    modeWFHBtn.addEventListener('click', () => {
      gpsMode = 'wfh';
      modeWFHBtn.classList.add('active');
      modeOfficeBtn.classList.remove('active');
      gpsStatusBox.textContent = '🏠 Working from home today';
    });

    gpsCheckinBtn.addEventListener('click', () => {
      if(gpsMode === 'wfh'){
        submitCheckin(null, null);
        return;
      }
      if(!navigator.geolocation){
        gpsStatusBox.textContent = '❌ Geolocation not supported by this browser';
        return;
      }
      gpsStatusBox.textContent = '📍 Getting your location...';
      gpsCheckinBtn.disabled = true;
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          submitCheckin(pos.coords.latitude, pos.coords.longitude);
        },
        (err) => {
          gpsStatusBox.textContent = '❌ Location access denied. Please enable location permissions.';
          gpsCheckinBtn.disabled = false;
        },
        { enableHighAccuracy: true, timeout: 10000 }
      );
    });
  }

  function submitCheckin(lat, lng){
    fetch('/attendance/checkin', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      credentials: 'include',
      body: JSON.stringify({ location_type: gpsMode, latitude: lat, longitude: lng })
    })
    .then(r => r.json().then(data => ({ status: r.status, data })))
    .then(({status, data}) => {
      gpsCheckinBtn.disabled = false;
      if(status === 201){
        gpsStatusBox.innerHTML = `✅ Checked in successfully ${data.distance ? '('+data.distance+'m from office)' : '(WFH)'}`;
        gpsCheckinBtn.textContent = '✓ Checked In';
        gpsCheckinBtn.disabled = true;
        showToast('Attendance marked!', 'success');
        loadAttendanceToday();
      } else {
        gpsStatusBox.textContent = '❌ ' + data.error;
        showToast(data.error, 'danger');
      }
    })
    .catch(() => {
      gpsCheckinBtn.disabled = false;
      gpsStatusBox.textContent = '❌ Something went wrong. Try again.';
    });
  }
'''

marker = "  checkSession();\n})();"
if marker in content:
    content = content.replace(marker, gps_js + "\n  checkSession();\n})();")
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ GPS JS logic added")
else:
    print("❌ Marker not found, searching alt pattern")
