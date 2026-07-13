with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '<span class="brand-mark">EM</span>'
new = '<span class="brand-mark" style="padding:0;overflow:hidden;background:#fff;"><img src="/static/images/mcarbon_logo.jpg" alt="mCarbon" style="width:100%;height:100%;object-fit:cover;border-radius:inherit;"></span>'

count = content.count(old)
content = content.replace(old, new)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ Replaced {count} logo instance(s)")
