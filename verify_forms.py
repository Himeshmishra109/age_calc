import json

# Load calculators
with open('data/calculators.json', 'r') as f:
    calculators = json.load(f)

# Load JavaScript file
with open('static/calculator-forms.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

print('='*60)
print('CALCULATOR FORMS VERIFICATION')
print('='*60)

total = len(calculators)
found = 0
missing = []

for calc in calculators:
    calc_id = calc['id']
    # Check if calculator ID is in the JavaScript
    if f"calcId === '{calc_id}'" in js_content:
        found += 1
    else:
        missing.append(f"{calc_id} ({calc['name']})")

print(f'\nTotal Calculators: {total}')
print(f'Forms Implemented: {found}')
print(f'Missing Forms: {len(missing)}')
print(f'Coverage: {(found/total)*100:.1f}%')

if missing:
    print('\n❌ Missing Calculator Forms:')
    for m in missing[:20]:  # Show first 20
        print(f'  - {m}')
    if len(missing) > 20:
        print(f'  ... and {len(missing)-20} more')
else:
    print('\n✅ All calculator forms implemented!')

print('='*60)
