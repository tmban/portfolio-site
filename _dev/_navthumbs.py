import os, glob

repls = {
    'kv10.webp': 'kv10-solid.webp',
    'vd13.webp': 'vd13-solid.webp',
    'ar13.webp': 'ar13-solid.webp',
    'pl8.webp':  'pl8-solid.webp',
}

pages = []
for root, dirs, files in os.walk('.'):
    # skip asset/motion dirs to be safe; only top-level + project subfolders matter
    for f in files:
        if f.endswith('.html'):
            pages.append(os.path.join(root, f))

changed = 0
for p in pages:
    with open(p, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    edited = False
    for i, ln in enumerate(lines):
        if 'topnav__dd-thumb' in ln or 'topnav__mproj' in ln:
            new = ln
            for old, sol in repls.items():
                # avoid double-suffixing already-solid
                if old in new and old.replace('.webp','-solid.webp') not in new:
                    new = new.replace(old, sol)
            if new != ln:
                lines[i] = new
                edited = True
    if edited:
        with open(p, 'w', encoding='utf-8') as fh:
            fh.writelines(lines)
        changed += 1
        print('updated', p)

print('files changed:', changed)
