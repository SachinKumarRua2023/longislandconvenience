import json, subprocess

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0ZTcyODRlMS0zMDE3LTQ3MTAtOGM1Ny01MzlhMDVlZDE0ZDEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImFjNDJiYmE5LTgzOGItNGMyNy1hYTQ4LWZiMjVjNjNiYTFjNCIsImlhdCI6MTc3OTMzOTYzN30.ffR0_Zh4JH5zL5nyv2xIPrSUYzmXX_DDHvTUa7hTPao'
URL = 'https://countrycoveballoons.app.n8n.cloud/mcp-server/http'

def mcp(name, args, call_id):
    payload = json.dumps({'jsonrpc':'2.0','method':'tools/call','params':{'name':name,'arguments':args},'id':call_id})
    r = subprocess.run(['curl','-s','-X','POST',URL,
                        '-H',f'Authorization: Bearer {TOKEN}',
                        '-H','Content-Type: application/json',
                        '-H','Accept: application/json, text/event-stream',
                        '-d',payload], capture_output=True)
    out = r.stdout.decode('utf-8','ignore')
    for line in out.splitlines():
        if line.startswith('data:'):
            d = json.loads(line[6:])
            return json.loads(d['result']['content'][0]['text'])
    return None

wf_data = mcp('get_workflow_details', {'workflowId': '0IRXTfqzgX5PhLBk'}, 10)
nodes = {n['name']: n for n in wf_data['workflow']['nodes']}

push = nodes['Push to GitHub → Vercel Deploys']
p = push['parameters']
print('=== Push to GitHub node ===')
print('method:', p.get('method'))
print('url repr:', repr(p.get('url','')))
print('sendBody:', p.get('sendBody'))
print('specifyBody:', p.get('specifyBody'))
print('contentType:', p.get('contentType'))
print('jsonBody repr:', repr(p.get('jsonBody','')))
print('body repr:', repr(p.get('body','')))
print()
print('headerParameters:', json.dumps(p.get('headerParameters',{}), indent=2))
