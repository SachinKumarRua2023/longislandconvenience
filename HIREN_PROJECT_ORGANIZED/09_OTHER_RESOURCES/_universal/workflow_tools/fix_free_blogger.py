import json, subprocess

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0ZTcyODRlMS0zMDE3LTQ3MTAtOGM1Ny01MzlhMDVlZDE0ZDEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImFjNDJiYmE5LTgzOGItNGMyNy1hYTQ4LWZiMjVjNjNiYTFjNCIsImlhdCI6MTc3OTMzOTYzN30.ffR0_Zh4JH5zL5nyv2xIPrSUYzmXX_DDHvTUa7hTPao'
URL = 'https://countrycoveballoons.app.n8n.cloud/mcp-server/http'
WORKFLOW_ID = '0IRXTfqzgX5PhLBk'

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

# Fetch current live workflow
print("Fetching workflow...")
wf_data = mcp('get_workflow_details', {'workflowId': WORKFLOW_ID}, 10)
nodes = {n['name']: n for n in wf_data['workflow']['nodes']}
top5_js    = nodes['Top 5 Stories']['parameters']['jsCode']
parse_js   = nodes['Parse Post JSON']['parameters']['jsCode']
format_js  = nodes['Format as TSX Page']['parameters']['jsCode']
print(f"top5={len(top5_js)}, parse={len(parse_js)}, format={len(format_js)}")

# ── Free Blog Generator — no API key needed ───────────────────────────────────
FREE_BLOGGER_JS = r"""
const { brief, today } = $input.first().json;

// Parse all 5 stories from the brief
const stories = brief.split('\n\n').filter(s => s.trim());

// Extract title and snippet from each story
const parsed = stories.map(story => {
  const lines = story.split('\n').filter(l => l.trim());
  const title = lines[0].replace(/^\d+\.\s+/, '').trim();
  const snippet = lines.slice(1).map(l => l.replace(/^\s+/, '')).join(' ').trim();
  return { title, snippet };
});

const top = parsed[0] || { title: 'Tech News Today', snippet: 'Latest tech updates.' };

// Build slug
const slug = today + '-' + top.title.toLowerCase()
  .replace(/[^a-z0-9\s]/g, '')
  .replace(/\s+/g, '-')
  .slice(0, 50)
  .replace(/-+$/, '');

// Primary keyword = first 3 meaningful words
const stopWords = new Set(['a','an','the','is','in','on','at','to','for','of','and','or','but','how','why','what','when','will']);
const primaryKeyword = top.title.split(/\s+/)
  .filter(w => !stopWords.has(w.toLowerCase()) && w.length > 2)
  .slice(0, 3).join(' ').toLowerCase();

const tags = ['tech news', 'technology', 'AI', 'programming', today.slice(0,4)];

const metaDescription = (top.snippet.slice(0, 140) + '...').replace(/\n/g, ' ');

// Other stories for the "More News" section
const otherStories = parsed.slice(1).map(s =>
  `- **${s.title}** — ${s.snippet.slice(0, 120)}${s.snippet.length > 120 ? '...' : ''}`
).join('\n');

const faqSchema = [
  {
    q: `What is happening with ${primaryKeyword}?`,
    a: top.snippet.slice(0, 300) || 'See full story above.'
  },
  {
    q: 'How does this affect developers and tech learners?',
    a: `Staying updated on ${primaryKeyword} is crucial for developers. At SeekhoWithRua, we cover these trends in our courses so you can apply the latest knowledge to real projects.`
  },
  {
    q: 'Where can I learn more about these tech topics?',
    a: 'Visit SeekhoWithRua LMS at https://lms.seekhowithrua.com for hands-on courses on Python, AI, Data Science, and Web Development.'
  }
];

const faqMd = '\n\n---\n## Frequently Asked Questions\n\n' +
  faqSchema.map(f => `**Q: ${f.q}**\n\n${f.a}\n`).join('\n');

const content = `## TL;DR
${top.snippet.slice(0, 200)}

## ${top.title}

${top.snippet}

As technology evolves rapidly, understanding **${primaryKeyword}** has become essential for every developer and tech enthusiast. At [SeekhoWithRua](https://seekhowithrua.com), we break down complex tech topics so you can learn and apply them faster.

## Why ${primaryKeyword} Matters in ${today.slice(0,4)}

The tech landscape is shifting. Here's what you need to know:

- Stay ahead by following **${primaryKeyword}** developments closely
- Apply these insights in your real-world projects
- Learn the underlying skills at [our LMS](https://lms.seekhowithrua.com)

## More Tech Headlines Today

${otherStories || '- Check back for more stories.'}

## Start Learning Today

Whether you're a beginner or experienced developer, SeekhoWithRua has structured courses in Python, AI, Data Science, and Web Development. **[Join free →](https://lms.seekhowithrua.com)**
${faqMd}`;

// Output in Claude-API-compatible format so Parse Post JSON works unchanged
const post = { title: top.title, slug, metaDescription, content, primaryKeyword, tags, faqSchema };
return [{ json: { content: [{ type: 'text', text: JSON.stringify(post) }] } }];
"""

# Load code for other nodes
top5_js_json   = json.dumps(top5_js)
parse_js_json  = json.dumps(parse_js)
format_js_json = json.dumps(format_js)
blogger_js_json = json.dumps(FREE_BLOGGER_JS.strip())

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
    parameters: {{ jsCode: {top5_js_json} }} }},
  output: [{{ brief: 'sample', today: '2026-05-21' }}] }});
const generateBlogPost = node({{ type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Generate Blog Post (Claude)', id: 'openai-1', position: [1104, 352],
    parameters: {{ jsCode: {blogger_js_json} }} }},
  output: [{{}}] }});
const parsePostJSON = node({{ type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Parse Post JSON', id: 'code-2', position: [1328, 352],
    parameters: {{ jsCode: {parse_js_json} }} }}, output: [{{}}] }});
const formatTSX = node({{ type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Format as TSX Page', id: 'format-tsx', position: [1552, 352],
    parameters: {{ jsCode: {format_js_json} }} }}, output: [{{}}] }});
const pushToGitHub = node({{ type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: {{ name: 'Push to GitHub → Vercel Deploys', id: 'github-push', position: [1776, 352],
    parameters: {{
      method: 'PUT',
      url: '=https://api.github.com/repos/SachinKumarRua2023/seekhowithrua-seo/contents/app/blog/{{{{ $json.slug }}}}/page.tsx',
      sendHeaders: true,
      headerParameters: {{ parameters: [
        {{ name: 'Authorization', value: '<__PLACEHOLDER_VALUE__token YOUR_GITHUB_PERSONAL_ACCESS_TOKEN__>' }},
        {{ name: 'Accept', value: 'application/vnd.github.v3+json' }},
        {{ name: 'X-GitHub-Api-Version', value: '2022-11-28' }}
      ] }},
      sendBody: true, specifyBody: 'json',
      jsonBody: '={{{{\\n  \\"message\\": \\"feat: auto blog post — {{{{ $json.title }}}}\\",\\n  \\"content\\": \\"{{{{ Buffer.from($json.tsxContent).toString(\\'base64\\') }}}}\\",\\n  \\"branch\\": \\"main\\"\\n}}}}',
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

print("\nValidating...")
val = mcp('validate_workflow', {'code': sdk}, 50)
if val is None:
    print("ERROR: validate returned None"); exit(1)
print(f"Valid: {val.get('valid')}")
if val.get('errors'):
    print("Errors:", val['errors']); exit(1)

print("Pushing...")
res = mcp('update_workflow', {'workflowId': WORKFLOW_ID, 'code': sdk,
          'name': 'Daily Tech Blog Auto-Poster — SeekhoWithRua SEO'}, 51)
print(f"Done! id={res.get('id') if res else 'ERROR'}")
