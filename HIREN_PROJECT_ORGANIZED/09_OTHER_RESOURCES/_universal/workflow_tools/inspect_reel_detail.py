import json

with open(r'C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\reel_active.txt', encoding='utf-8') as f:
    raw = f.read()

data = None
for line in raw.splitlines():
    if line.startswith('data:'):
        data = json.loads(line[6:])
        break

wf = json.loads(data['result']['content'][0]['text'])['workflow']

print('=== ACTIVE REEL CREATOR — FULL NODE DETAILS ===\n')
for n in wf['nodes']:
    print('NODE: ' + n['name'])
    print('  type: ' + n['type'])
    p = n.get('parameters', {})
    # Print all parameters
    for k, v in p.items():
        if isinstance(v, str):
            val = v[:300].replace('\n', '\\n')
            print('  ' + k + ': ' + val)
        elif isinstance(v, dict):
            print('  ' + k + ': ' + json.dumps(v)[:300])
        else:
            print('  ' + k + ': ' + str(v)[:200])
    # Special: check for credentials
    creds = n.get('credentials', {})
    if creds:
        print('  CREDENTIALS: ' + str(creds))
    print()

# Print connections
print('=== CONNECTIONS ===')
for src, conns in wf.get('connections', {}).items():
    for i, arr in enumerate(conns.get('main', [])):
        for c in arr:
            print(src + ' -[main:' + str(i) + ']-> ' + c['node'])

# activeVersion node check
av = wf.get('activeVersion', {})
if av:
    print('\n=== ACTIVE VERSION NODE COUNT: ' + str(len(av.get('nodes',[]))) + ' ===')
    av_conns = av.get('connections', {})
    print('activeVersion connections:')
    for src, conns in av_conns.items():
        for i, arr in enumerate(conns.get('main', [])):
            for c in arr:
                print('  AV: ' + src + ' -[main:' + str(i) + ']-> ' + c['node'])
