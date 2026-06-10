import json, subprocess

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0ZTcyODRlMS0zMDE3LTQ3MTAtOGM1Ny01MzlhMDVlZDE0ZDEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImFjNDJiYmE5LTgzOGItNGMyNy1hYTQ4LWZiMjVjNjNiYTFjNCIsImlhdCI6MTc3OTMzOTYzN30.ffR0_Zh4JH5zL5nyv2xIPrSUYzmXX_DDHvTUa7hTPao'
URL_MCP = 'https://countrycoveballoons.app.n8n.cloud/mcp-server/http'
WORKFLOW_ID = '0IRXTfqzgX5PhLBk'

def mcp(name, args, call_id):
    payload = json.dumps({'jsonrpc':'2.0','method':'tools/call','params':{'name':name,'arguments':args},'id':call_id})
    r = subprocess.run(['curl','-s','-X','POST',URL_MCP,
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

print('Fetching blog workflow...')
wf_data = mcp('get_workflow_details', {'workflowId': WORKFLOW_ID}, 10)
nodes = {n['name']: n for n in wf_data['workflow']['nodes']}

top5_js   = nodes['Top 5 Stories']['parameters']['jsCode']
parse_js  = nodes['Parse Post JSON']['parameters']['jsCode']
format_js = nodes['Format as TSX Page']['parameters']['jsCode']
print(f'top5={len(top5_js)}, parse={len(parse_js)}, format={len(format_js)}')

# ── Fixed GitHub node params ─────────────────────────────────────────────────
# URL: no = prefix — n8n handles {{ }} template syntax natively in URL fields
GITHUB_URL = 'https://api.github.com/repos/SachinKumarRua2023/seekhowithrua-seo/contents/app/blog/{{ $json.slug }}/page.tsx'

# jsonBody: no = prefix, no {{ }} nesting — plain JSON template with {{ }} expressions
GITHUB_BODY = '{\n  "message": "feat: auto blog post — {{ $json.title }}",\n  "content": "{{ Buffer.from($json.tsxContent).toString(\'base64\') }}",\n  "branch": "main"\n}'

print('URL prefix:', GITHUB_URL[:50])
print('Body prefix:', GITHUB_BODY[:60])

# jsonBody for Generate Blog Post — properly escaped, no raw newlines
SYSTEM_PROMPT = (
    "You are an expert SEO and GEO (Generative Engine Optimization) tech blogger for SeekhoWithRua "
    "— a tech education platform. Write engaging blog posts optimized for BOTH traditional search "
    "engines (Google) AND AI answer engines (ChatGPT, Perplexity, Claude, Gemini).\n\n"
    "SEO requirements:\n"
    "- Target 1 primary keyword + 3-5 LSI keywords\n"
    "- Use keyword in title, first paragraph, one H2, meta description\n"
    "- Include internal link placeholder: [Join our LMS](https://lms.seekhowithrua.com)\n"
    "- 800-1000 words, short paragraphs, scannable\n\n"
    "GEO requirements (AI engine optimization):\n"
    "- Start with a clear direct answer to the implied question (answer-first structure)\n"
    "- Include a structured FAQ section at the end with 3 Q&A pairs\n"
    "- Use factual, citation-worthy statements\n"
    "- Add a TL;DR summary at the top\n"
    "- Use clear H2/H3 headings that match likely AI queries\n"
    "- Include numbered lists and bullet points for featured snippet capture\n\n"
    "Tone: Friendly, educational, expert. Target: aspiring developers in USA."
)
USER_CONTENT = (
    "Today: {{ $json.today }}\n\n"
    "Latest Tech News:\n{{ $json.brief }}\n\n"
    "Write a complete SEO+GEO optimized blog post. Return ONLY this JSON (no extra text):\n"
    "{\"title\":\"...\",\"slug\":\"kebab-case\",\"metaDescription\":\"max 155 chars with primary keyword\","
    "\"content\":\"full markdown with TL;DR, H2s, FAQ section\",\"primaryKeyword\":\"...\","
    "\"tags\":[\"tag1\",\"tag2\",\"tag3\"],\"faqSchema\":[{\"q\":\"...\",\"a\":\"...\"}]}"
)
json_body_obj = {
    "model": "claude-opus-4-7",
    "max_tokens": 2000,
    "system": SYSTEM_PROMPT,
    "messages": [{"role": "user", "content": USER_CONTENT}]
}
GEN_JSON_BODY = '=' + json.dumps(json_body_obj, ensure_ascii=False)
assert '\n' not in GEN_JSON_BODY

# json.dumps all string params for safe JS embedding
top5_json    = json.dumps(top5_js)
parse_json   = json.dumps(parse_js)
format_json  = json.dumps(format_js)
gen_jb_json  = json.dumps(GEN_JSON_BODY)
gh_url_json  = json.dumps(GITHUB_URL)
gh_body_json = json.dumps(GITHUB_BODY)

sdk = f"""import {{ workflow, node, trigger, merge }} from '@n8n/workflow-sdk';

const dailyTrigger = trigger({{
  type: 'n8n-nodes-base.scheduleTrigger', version: 1.1,
  config: {{ name: 'Daily 8AM', id: 'cron-1', position: [208, 352],
    parameters: {{ rule: {{ interval: [{{ field: 'cronExpression', expression: '0 8 * * *' }}] }} }} }},
  output: [{{}}]
}});
const techCrunch = node({{ type: 'n8n-nodes-base.rssFeedRead', version: 1,
  config: {{ name: 'TechCrunch', id: 'rss-tc', position: [432, 160],
    parameters: {{ url: 'https://feeds.feedburner.com/TechCrunch', options: {{}} }} }}, output: [{{}}] }});
const hackerNews = node({{ type: 'n8n-nodes-base.rssFeedRead', version: 1,
  config: {{ name: 'Hacker News', id: 'rss-hn', position: [432, 352],
    parameters: {{ url: 'https://hnrss.org/frontpage', options: {{}} }} }}, output: [{{}}] }});
const theVerge = node({{ type: 'n8n-nodes-base.rssFeedRead', version: 1,
  config: {{ name: 'The Verge', id: 'rss-vg', position: [432, 544],
    parameters: {{ url: 'https://www.theverge.com/rss/index.xml', options: {{}} }} }}, output: [{{}}] }});
const mergeNews = merge({{ version: 3,
  config: {{ name: 'Merge News', id: '3f8dac4b-3854-4323-8609-dd2fb66efaad', position: [656, 336],
    parameters: {{ numberInputs: 3 }} }} }});
const top5Stories = node({{ type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Top 5 Stories', id: 'code-1', position: [880, 352], alwaysOutputData: true,
    parameters: {{ jsCode: {top5_json} }} }},
  output: [{{ brief: 'sample', today: '2026-05-22' }}] }});
const generateBlogPost = node({{ type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Generate Blog Post (Claude)', id: 'openai-1', position: [1104, 352],
    parameters: {{ jsCode: {json.dumps(nodes['Generate Blog Post (Claude)']['parameters']['jsCode'])} }} }},
  output: [{{}}] }});
const parsePostJSON = node({{ type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Parse Post JSON', id: 'code-2', position: [1328, 352],
    parameters: {{ jsCode: {parse_json} }} }}, output: [{{}}] }});
const formatTSX = node({{ type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Format as TSX Page', id: 'format-tsx', position: [1552, 352],
    parameters: {{ jsCode: {format_json} }} }}, output: [{{}}] }});
const pushToGitHub = node({{ type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: {{ name: 'Push to GitHub → Vercel Deploys', id: 'github-push', position: [1776, 352],
    parameters: {{
      method: 'PUT',
      url: {gh_url_json},
      sendHeaders: true,
      headerParameters: {{ parameters: [
        {{ name: 'Authorization', value: '<__PLACEHOLDER_VALUE__token YOUR_GITHUB_PERSONAL_ACCESS_TOKEN__>' }},
        {{ name: 'Accept', value: 'application/vnd.github.v3+json' }},
        {{ name: 'X-GitHub-Api-Version', value: '2022-11-28' }}
      ] }},
      sendBody: true, specifyBody: 'json',
      jsonBody: {gh_body_json},
      options: {{}}
    }}
  }}, output: [{{}}] }});
const emailConfirmation = node({{ type: 'n8n-nodes-base.emailSend', version: 2.1,
  config: {{ name: 'Email Confirmation', id: 'email-1', position: [2000, 352],
    alwaysOutputData: true, executeOnce: true, retryOnFail: true,
    parameters: {{
      operation: 'sendAndWait',
      fromEmail: 'sachinkumarrua@gmail.com', toEmail: 'sachinkumarrua@gmail.com',
      subject: "=✅ Blog Posted: {{{{ $('Parse Post JSON').item.json.title }}}}",
      message: '✅ Blog Posted', options: {{}}
    }}
  }}, output: [{{}}] }});

export default workflow('{WORKFLOW_ID}', 'Daily Tech Blog Auto-Poster — SeekhoWithRua SEO')
  .add(dailyTrigger)
  .to(techCrunch.to(mergeNews.input(0)))
  .add(dailyTrigger)
  .to(hackerNews.to(mergeNews.input(1)))
  .add(dailyTrigger)
  .to(theVerge.to(mergeNews.input(2)))
  .add(mergeNews)
  .to(top5Stories)
  .to(generateBlogPost)
  .to(parsePostJSON)
  .to(formatTSX)
  .to(pushToGitHub)
  .to(emailConfirmation);
"""

print('\nValidating...')
val = mcp('validate_workflow', {'code': sdk}, 50)
if val is None:
    print('ERROR: validate returned None'); exit(1)
print('Valid:', val.get('valid'))
if val.get('errors'):
    print('Errors:', val['errors']); exit(1)

print('Pushing...')
res = mcp('update_workflow', {'workflowId': WORKFLOW_ID, 'code': sdk,
          'name': 'Daily Tech Blog Auto-Poster — SeekhoWithRua SEO'}, 51)
print('Done!', str(res)[:200] if res else 'ERROR')
