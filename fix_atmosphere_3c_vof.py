import os, glob, re

boundary_templates = {
    'volScalarField': '''
    atmosphere
    {
        type            zeroGradient;
    }''',
    'volVectorField': '''
    atmosphere
    {
        type            zeroGradient;
    }'''
}

for filepath in glob.glob("0_org/*"):
    if not os.path.isfile(filepath):
        continue
    with open(filepath, 'r') as f:
        content = f.read()

    if 'atmosphere' not in content and 'boundaryField' in content:
        # Insert atmosphere patch inside boundaryField right before frontAndBack or closing bracket
        if 'frontAndBack' in content:
            content = content.replace('frontAndBack', boundary_templates['volScalarField'] + '\n    frontAndBack')
        else:
            content = re.sub(r'(boundaryField\s*\{)', r'\1\n' + boundary_templates['volScalarField'], content)
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Added atmosphere patch to {filepath}")

print("All 0_org boundary fields verified!")
