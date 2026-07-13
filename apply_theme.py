import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Core color variables -> dark neon
    ("--bg:#F6F7FC;--surface:#FFFFFF;--surface-alt:#F1F2FA;--border:#E6E8F5;",
     "--bg:#0a0e1a;--surface:#141a2e;--surface-alt:#1b2340;--border:rgba(168,85,247,.25);"),

    ("--text:#1D2333;--text-muted:#6B7280;--primary:#4F46E5;--primary-light:#6D64F0;--primary-dark:#3730A3;",
     "--text:#e2e8f0;--text-muted:#94a3b8;--primary:#a855f7;--primary-light:#c084fc;--primary-dark:#7e22ce;"),

    ("--accent:#12B886;--accent-dark:#0C9A70;--warning:#F5A524;--danger:#EF476F;",
     "--accent:#06b6d4;--accent-dark:#0891b2;--warning:#fbbf24;--danger:#f43f5e;"),

    ("--shadow-sm:0 1px 3px rgba(30,30,70,.05);--shadow-md:0 16px 40px rgba(79,70,229,.10);--shadow-glow:0 8px 24px rgba(79,70,229,.22);",
     "--shadow-sm:0 1px 3px rgba(0,0,0,.4);--shadow-md:0 16px 40px rgba(168,85,247,.18);--shadow-glow:0 8px 24px rgba(168,85,247,.35);"),

    # Floating orb colors -> neon purple/cyan/pink
    ("#C7D2FE,transparent 70%", "#a855f7,transparent 70%"),
    ("#99F6E4,transparent 70%", "#06b6d4,transparent 70%"),
    ("#FBCFE8,transparent 70%", "#ec4899,transparent 70%"),

    # Slightly brighter orbs since dark bg absorbs light
    ("opacity:.35;z-index:0", "opacity:.55;z-index:0"),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
    else:
        print(f"⚠️  NOT FOUND: {old[:60]}...")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Applied {count}/{len(replacements)} replacements")
