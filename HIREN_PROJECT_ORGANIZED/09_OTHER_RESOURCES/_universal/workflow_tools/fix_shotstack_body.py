import json, subprocess

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0ZTcyODRlMS0zMDE3LTQ3MTAtOGM1Ny01MzlhMDVlZDE0ZDEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImFjNDJiYmE5LTgzOGItNGMyNy1hYTQ4LWZiMjVjNjNiYTFjNCIsImlhdCI6MTc3OTMzOTYzN30.ffR0_Zh4JH5zL5nyv2xIPrSUYzmXX_DDHvTUa7hTPao'
URL = 'https://countrycoveballoons.app.n8n.cloud/mcp-server/http'
WORKFLOW_ID = 'wKPo6C79nSWV8K9M'
SHOTSTACK_KEY = '71bXjUcRMKS2yEp2ZEDXfTC0TPychF6cQ4aUuOjb'

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

# Fetch current workflow to preserve all code nodes
print('Fetching workflow...')
wf_data = mcp('get_workflow_details', {'workflowId': WORKFLOW_ID}, 10)
nodes = {n['name']: n for n in wf_data['workflow']['nodes']}
parse_js    = nodes['Parse & Build Row']['parameters']['jsCode']
extract_js  = nodes['Extract Video URL']['parameters']['jsCode']
content_js  = nodes['Generate Trending Content']['parameters']['jsCode']

# ── Shotstack body — use json.dumps to avoid f-string brace escaping issues ──
# The n8n expression uses ={{ }} syntax; json.dumps handles all escaping
SHOTSTACK_BODY = '={{ JSON.stringify({ timeline: { background: \'#000000\', tracks: [{ clips: [{ asset: { type: \'image\', src: $json.data }, start: 0, length: 5, effect: \'zoomIn\' }] }] }, output: { format: \'mp4\', resolution: \'hd\', aspectRatio: \'9:16\' } }) }}'

# Verify the string starts correctly
assert SHOTSTACK_BODY.startswith('={{ '), f'Bad prefix: {SHOTSTACK_BODY[:10]}'
print('Shotstack body prefix OK:', SHOTSTACK_BODY[:30])

# json.dumps on all code/body strings — guarantees proper JS string literal
parse_js_json    = json.dumps(parse_js)
extract_js_json  = json.dumps(extract_js)
content_js_json  = json.dumps(content_js)
shotstack_body_json = json.dumps(SHOTSTACK_BODY)

sdk = """import { workflow, node, trigger } from '@n8n/workflow-sdk';

const manualTrigger = trigger({
  type: 'n8n-nodes-base.manualTrigger', version: 1,
  config: { name: 'Manual Trigger', id: 'manual-1', position: [0, 352], parameters: {} },
  output: [{}]
});

const scheduleTrigger = trigger({
  type: 'n8n-nodes-base.scheduleTrigger', version: 1.1,
  config: { name: 'Every Day 9AM', id: 'sched-1', position: [0, 160],
    parameters: { rule: { interval: [{ field: 'cronExpression', expression: '0 9 * * *' }] } } },
  output: [{}]
});

const generateContent = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Generate Trending Content', id: 'gen-content', position: [240, 256],
    parameters: { jsCode: """ + content_js_json + """ } },
  output: [{}]
});

const parseRow = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Parse & Build Row', id: 'parse-row', position: [480, 256],
    parameters: { jsCode: """ + parse_js_json + """ } },
  output: [{}]
});

const downloadImage = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: { name: 'Download Reel Image', id: 'dl-img', position: [720, 256],
    parameters: {
      url: '={{ $json.imageUrl }}',
      options: { response: { response: { responseFormat: 'file', outputPropertyName: 'imageData' } }, timeout: 120000 }
    }
  },
  output: [{}]
});

const uploadCatbox = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: { name: 'Upload to Catbox', id: 'upload-catbox', position: [960, 192],
    parameters: {
      method: 'POST',
      url: 'https://litterbox.catbox.moe/resources/internals/api.php',
      sendBody: true,
      contentType: 'multipart-form-data',
      bodyParameters: { parameters: [
        { name: 'reqtype', value: 'fileupload' },
        { name: 'time', value: '72h' },
        { parameterType: 'formBinaryData', name: 'fileToUpload', inputDataFieldName: 'imageData' }
      ] },
      options: { response: { response: { responseFormat: 'text' } } }
    }
  },
  output: [{}]
});

const saveImageDrive = node({
  type: 'n8n-nodes-base.googleDrive', version: 3,
  config: { name: 'Save Image to Drive', id: 'save-img', position: [960, 352],
    parameters: {
      operation: 'upload',
      inputDataFieldName: 'imageData',
      name: "={{ $('Parse & Build Row').item.json.Topic + ' - ' + $('Parse & Build Row').item.json.Date + '.jpg' }}",
      driveId: { '__rl': true, mode: 'list', value: 'My Drive' },
      folderId: { '__rl': true, value: '1gxbenDHHzUIxW4JqSc2h8_44hO2iPEwe', mode: 'list', cachedResultName: 'MY CONTENT' },
      options: {}
    }
  },
  output: [{}]
});

const createRender = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: { name: 'Create Shotstack Render', id: 'create-render', position: [1200, 192],
    parameters: {
      method: 'POST',
      url: 'https://api.shotstack.io/v1/render',
      sendHeaders: true,
      headerParameters: { parameters: [
        { name: 'x-api-key', value: '""" + SHOTSTACK_KEY + """' },
        { name: 'Content-Type', value: 'application/json' }
      ] },
      sendBody: true,
      contentType: 'raw',
      body: """ + shotstack_body_json + """,
      options: {}
    }
  },
  output: [{}]
});

const waitRender = node({
  type: 'n8n-nodes-base.wait', version: 1.1,
  config: { name: 'Wait for Render', id: 'wait-render', position: [1440, 192],
    parameters: { amount: 180 } },
  output: [{}]
});

const getRender = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: { name: 'Get Shotstack Render', id: 'get-render', position: [1680, 192],
    parameters: {
      url: "=https://api.shotstack.io/v1/render/{{ $('Create Shotstack Render').item.json.response.id }}",
      sendHeaders: true,
      headerParameters: { parameters: [
        { name: 'x-api-key', value: '""" + SHOTSTACK_KEY + """' }
      ] },
      options: {}
    }
  },
  output: [{}]
});

const extractUrl = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Extract Video URL', id: 'extract-url', position: [1920, 192],
    parameters: { jsCode: """ + extract_js_json + """ } },
  output: [{}]
});

const downloadVideo = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: { name: 'Download Video', id: 'dl-video', position: [2160, 192],
    parameters: {
      url: '={{ $json.videoUrl }}',
      options: { response: { response: { responseFormat: 'file', outputPropertyName: 'videoData' } }, timeout: 120000 }
    }
  },
  output: [{}]
});

const saveVideoDrive = node({
  type: 'n8n-nodes-base.googleDrive', version: 3,
  config: { name: 'Save Video to Drive', id: 'save-video', position: [2400, 192],
    parameters: {
      operation: 'upload',
      inputDataFieldName: 'videoData',
      name: "={{ $('Parse & Build Row').item.json.Topic + ' - ' + $('Parse & Build Row').item.json.Date + '.mp4' }}",
      driveId: { '__rl': true, mode: 'list', value: 'My Drive' },
      folderId: { '__rl': true, value: '1QSAOTPFBIg-kYlnSg3mchq2VU0cvFFb8', mode: 'list', cachedResultName: 'CONTENT VIDEO' },
      options: {}
    }
  },
  output: [{}]
});

export default workflow('""" + WORKFLOW_ID + """', 'Daily Reel Creator - Country Cove Balloons')
  .add(manualTrigger).to(generateContent)
  .add(scheduleTrigger).to(generateContent)
  .add(generateContent).to(parseRow)
  .add(parseRow).to(downloadImage)
  .add(downloadImage).to(uploadCatbox)
  .add(downloadImage).to(saveImageDrive)
  .add(uploadCatbox).to(createRender)
  .add(createRender).to(waitRender)
  .add(waitRender).to(getRender)
  .add(getRender).to(extractUrl)
  .add(extractUrl).to(downloadVideo)
  .add(downloadVideo).to(saveVideoDrive);
"""

# Verify the body is correctly embedded in the SDK
assert '={{ JSON.stringify(' in sdk, 'Body expression missing!'
print('Body expression found in SDK: OK')

print('\nValidating...')
val = mcp('validate_workflow', {'code': sdk}, 50)
if val is None:
    print('ERROR: validate returned None'); exit(1)
print('Valid: ' + str(val.get('valid')))
if val.get('errors'):
    print('Errors: ' + str(val['errors'])); exit(1)

print('Pushing...')
res = mcp('update_workflow', {'workflowId': WORKFLOW_ID, 'code': sdk,
          'name': 'Daily Reel Creator - Country Cove Balloons'}, 51)
print('Done! ' + str(res)[:200] if res else 'ERROR')
