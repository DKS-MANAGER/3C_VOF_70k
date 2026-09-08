import os, glob, re

for filepath in glob.glob("0_org/*"):
    if not os.path.isfile(filepath):
        continue
    filename = os.path.basename(filepath)
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace object line in FoamFile dictionary with exact filename
    content = re.sub(r'object\s+[a-zA-Z0-9_\.]+;', f'object      {filename};', content)

    with open(filepath, 'w') as f:
        f.write(content)

print("All object headers matched to filenames successfully!")
