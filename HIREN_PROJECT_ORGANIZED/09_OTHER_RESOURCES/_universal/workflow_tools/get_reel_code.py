import json

with open(r'C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\reel_active.txt', encoding='utf-8') as f:
    raw = f.read()

data = None
for line in raw.splitlines():
    if line.startswith('data:'):
        data = json.loads(line[6:])
        break

wf = json.loads(data['result']['content'][0]['text'])['workflow']
nodes = {n['name']: n for n in wf['nodes']}

# Print full code nodes
for name in ['Parse & Build Row', 'Extract Video URL']:
    code = nodes[name]['parameters'].get('jsCode','')
    print('=== ' + name + ' ===')
    print(code)
    print()

# Print full Generate Trending Content prompt
gen = nodes['Generate Trending Content']['parameters']
print('=== Generate Trending Content messages ===')
print(json.dumps(gen.get('messages', {}), indent=2))
print()
print('Model:', json.dumps(gen.get('modelId',{})))
print()

# Print credentials info
print('=== Credentials per node ===')
for n in wf['nodes']:
    creds = n.get('credentials', {})
    if creds:
        print(n['name'] + ': ' + json.dumps(creds))
    else:
        print(n['name'] + ': NO CREDENTIALS')
