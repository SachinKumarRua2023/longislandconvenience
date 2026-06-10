import json

for fname, label in [('reel_active.txt','ACTIVE'), ('reel_inactive.txt','INACTIVE')]:
    with open(r'C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\\' + fname, encoding='utf-8') as f:
        raw = f.read()
    data = None
    for line in raw.splitlines():
        if line.startswith('data:'):
            data = json.loads(line[6:])
            break
    if not data:
        print(label + ': could not parse'); continue
    wf = json.loads(data['result']['content'][0]['text'])['workflow']
    print('\n=== ' + label + ' [' + wf['id'] + '] ===')
    print('Name: ' + wf['name'])
    print('Active: ' + str(wf['active']))
    print('Nodes:')
    for n in wf['nodes']:
        t = n['type'].replace('n8n-nodes-base.','')
        p = n.get('parameters', {})
        issues = []
        for k, v in p.items():
            if isinstance(v, str) and '__PLACEHOLDER_VALUE__' in v:
                issues.append('PLACEHOLDER in ' + k)
            if isinstance(v, dict):
                for hdr in v.get('parameters', []):
                    if '__PLACEHOLDER_VALUE__' in str(hdr.get('value', '')):
                        issues.append('PLACEHOLDER in ' + str(hdr.get('name','')))
        hp = p.get('headerParameters', {}).get('parameters', [])
        for hdr in hp:
            if '__PLACEHOLDER_VALUE__' in str(hdr.get('value', '')):
                issues.append('PLACEHOLDER header: ' + str(hdr.get('name','')))
        issue_str = ' *** ' + str(issues) if issues else ''
        print('  - ' + n['name'] + ' (' + t + ')' + issue_str)
    print('Connections:')
    for src, conns in wf.get('connections', {}).items():
        targets = [c['node'] for arr in conns.get('main', []) for c in arr]
        print('  ' + src + ' -> ' + str(targets))
    # Also show activeVersion connections if different
    av = wf.get('activeVersion', {})
    if av:
        av_conns = av.get('connections', {})
        if av_conns != wf.get('connections', {}):
            print('activeVersion connections DIFFER:')
            for src, conns in av_conns.items():
                targets = [c['node'] for arr in conns.get('main', []) for c in arr]
                print('  AV: ' + src + ' -> ' + str(targets))
