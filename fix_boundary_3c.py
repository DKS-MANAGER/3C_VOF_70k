import os, glob, re

for filepath in glob.glob("0_org/*"):
    if not os.path.isfile(filepath):
        continue
    with open(filepath, 'r') as f:
        text = f.read()

    text = text.replace('leftWall', 'inlet')
    text = text.replace('rightWall', 'outlet')
    text = text.replace('lowerWallSmooth', 'bottom')
    text = text.replace('lowerWallRough', 'bridgeDeck')
    text = text.replace('cfrontWall', 'frontAndBack')

    # Remove cbackWall entry (keyword + block)
    text = re.sub(r'cbackWall\s*\{[^}]*\}', '', text)

    # Ensure bridgeDeck exists if bottom exists and bridgeDeck does not
    if 'bottom' in text and 'bridgeDeck' not in text:
        match = re.search(r'(bottom\s*\{[^}]*\})', text)
        if match:
            bottom_block = match.group(1)
            bridge_block = bottom_block.replace('bottom', 'bridgeDeck')
            text = text.replace(bottom_block, bottom_block + '\n    ' + bridge_block)

    # Fix wall function on outlet/inlet for turbulence fields
    if "nut.fluid" in filepath:
        text = re.sub(r'outlet\s*\{[^}]*\}', 'outlet\n    {\n        type            calculated;\n        value           uniform 0;\n    }', text)
        text = re.sub(r'inlet\s*\{[^}]*\}', 'inlet\n    {\n        type            calculated;\n        value           uniform 0;\n    }', text)

    text = text.replace('epsilonWallFunction', 'zeroGradient')
    text = text.replace('kqRWallFunction', 'zeroGradient')
    text = text.replace('nutUSpaldingWallFunction', 'calculated')

    with open(filepath, 'w') as f:
        f.write(text)

print("Regex boundary fix applied cleanly!")
