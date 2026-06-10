import json, subprocess

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0ZTcyODRlMS0zMDE3LTQ3MTAtOGM1Ny01MzlhMDVlZDE0ZDEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImFjNDJiYmE5LTgzOGItNGMyNy1hYTQ4LWZiMjVjNjNiYTFjNCIsImlhdCI6MTc3OTMzOTYzN30.ffR0_Zh4JH5zL5nyv2xIPrSUYzmXX_DDHvTUa7hTPao'
URL = 'https://countrycoveballoons.app.n8n.cloud/mcp-server/http'
WORKFLOW_ID = 'wKPo6C79nSWV8K9M'

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

# Fetch current workflow to preserve Parse & Build Row and Extract Video URL code
print('Fetching reel workflow...')
wf_data = mcp('get_workflow_details', {'workflowId': WORKFLOW_ID}, 10)
nodes = {n['name']: n for n in wf_data['workflow']['nodes']}
parse_js = nodes['Parse & Build Row']['parameters']['jsCode']
extract_js = nodes['Extract Video URL']['parameters']['jsCode']
print(f'parse_js len={len(parse_js)}, extract_js len={len(extract_js)}')

# ── Free content generator — no API needed ───────────────────────────────────
HASHTAGS = '#balloon #balloonart #balloondecorations #birthdayballoons #partyballoons #balloonbouquet #eventdecor #balloondesign #balloonartist #partydecor #celebrationballoons #balloonlove #countrycoveballoons #balloonbusiness #giftideas #partyplanning #balloonarrangement #weddingdecor #babyshower #corporateevents #balloonwall #organicballoons #balloongarland #luxurydecor #ballooninstallation #partyinspo #eventplanner #balloondelivery #DIYballoons #balloontrends'

FREE_CONTENT_JS = r"""
const HASHTAGS = '""" + HASHTAGS + r"""';

const topics = [
  { topic: 'Birthday Balloon Arch', title: 'This Birthday Arch Will Leave Them Speechless', caption: "Turn any birthday into an unforgettable moment! 🎂✨ Our custom balloon arches transform any space into pure magic. DM us to book your dream setup!", imagePrompt: 'photorealistic professional photograph of stunning luxury birthday balloon arch in blush pink champagne gold and white, elegant grand venue, chandeliers, ultra detailed 8k', tip: 'Mix chrome and matte balloons together for a high-end, professional look', postType: 'Reel' },
  { topic: 'Wedding Balloon Garland', title: 'Wedding Balloon Goals That Will WOW Your Guests', caption: "Your wedding deserves the most beautiful details! 💍🎈 Our organic balloon garlands add the perfect romantic touch to your big day. Let's create your dream wedding together!", imagePrompt: 'photorealistic professional photograph of breathtaking wedding balloon garland in ivory white dusty rose and sage green, romantic ceremony hall, soft candlelight, ultra detailed 8k', tip: 'Use neutral tones like ivory, sage and blush for elegant wedding balloon setups', postType: 'Reel' },
  { topic: 'Baby Shower Balloon Wall', title: 'Baby Shower Setup So Cute You Will Cry', caption: "Celebrate the new arrival in style! 👶🎈 Our custom baby shower balloon walls create the most adorable photo moments. Book now and make it extra special!", imagePrompt: 'photorealistic professional photograph of magical baby shower balloon wall in pastel yellow mint and white, gender neutral nursery setting, soft natural light, ultra detailed 8k', tip: 'Pastel balloon walls photograph beautifully — use soft ring lights for extra glow', postType: 'Reel' },
  { topic: 'Graduation Balloon Column', title: 'Graduation Party That Goes VIRAL on Social Media', caption: "They worked so hard — celebrate them BIG! 🎓🎉 Our graduation balloon columns are the ultimate party statement. Surprise your grad today!", imagePrompt: 'photorealistic professional photograph of tall elegant graduation balloon columns in royal blue silver and gold, festive celebration hall, confetti, ultra detailed 8k', tip: 'Add personalized banners between balloon columns for a unique graduation look', postType: 'Reel' },
  { topic: 'Corporate Event Balloons', title: 'Transform Your Office Into A Celebration Space', caption: "Impress clients and boost team morale! 🏢🎈 Our corporate balloon setups elevate any business event. Professional, branded, and unforgettable!", imagePrompt: 'photorealistic professional photograph of sophisticated corporate event balloon decoration in navy blue silver and white, modern conference hall, professional lighting, ultra detailed 8k', tip: 'Match balloon colors exactly to your brand colors for cohesive corporate events', postType: 'Reel' },
  { topic: 'Proposal Balloon Setup', title: 'He Said YES! The Most Romantic Setup EVER', caption: "Make the most important question even more magical! 💍💕 Our custom proposal balloon setups create the perfect moment. She'll say YES every time!", imagePrompt: 'photorealistic professional photograph of ultra romantic proposal balloon setup with rose gold red and pink heart balloons, fairy lights candles and rose petals, intimate candlelit room, ultra detailed 8k', tip: 'Heart-shaped balloon clusters with fairy lights create the most romantic proposal backdrops', postType: 'Reel' },
  { topic: 'Sweet 16 Balloon Decor', title: 'Sweet 16 Party Setup That Hits Different', caption: "Turn 16 into a moment she will NEVER forget! 🎀✨ Our Sweet 16 setups are pure magic. From balloon arches to full room transformations — we do it all!", imagePrompt: 'photorealistic professional photograph of glamorous sweet 16 birthday balloon decoration in hot pink purple gold and white, luxury ballroom, disco ball reflections, ultra detailed 8k', tip: 'Metallic balloon letters spelling the name create the ultimate Sweet 16 focal point', postType: 'Reel' },
  { topic: 'Anniversary Balloon Surprise', title: 'Anniversary Surprise That Will Make Them Cry Happy Tears', caption: "Because some moments deserve to be extra special! 💑🎈 Surprise your partner with a stunning balloon setup on your anniversary. Love is always worth celebrating!", imagePrompt: 'photorealistic professional photograph of romantic anniversary balloon room decoration with red rose gold and pink balloons, heart balloon sculpture, rose petals on floor, ultra detailed 8k', tip: 'Balloon letter numbers (years together) make anniversary setups deeply personal', postType: 'Reel' },
  { topic: 'Organic Balloon Bouquet', title: 'Why Organic Balloon Bouquets Are Taking Over', caption: "Classic meets modern! 🌿🎈 Our organic balloon bouquets are the hottest trend in celebration decor right now. Perfect for any occasion, any size space!", imagePrompt: 'photorealistic professional photograph of stunning organic balloon bouquet arrangement in terracotta burnt orange peach and cream colors, modern minimalist interior, natural light, ultra detailed 8k', tip: 'Organic clusters look best with 3 sizes of balloons — small, medium, and large', postType: 'Reel' },
  { topic: 'Balloon Ceiling Installation', title: 'Your Guests Will Look UP and GASP', caption: "Take the party to new heights — literally! 🎈☁️ Our balloon ceiling installations create the most jaw-dropping entrance moments. Make your event legendary!", imagePrompt: 'photorealistic professional photograph of spectacular balloon ceiling installation covering entire ceiling in pastel rainbow colors, grand ballroom below filled with guests, magical atmosphere, ultra detailed 8k', tip: 'Ceiling balloon clouds work best with a mix of 11 inch and 5 inch balloons for depth', postType: 'Reel' },
  { topic: 'Number Balloon Display', title: 'These Number Balloons Are Absolutely STUNNING', caption: "Make the number count! 🔢✨ Our jumbo number balloon displays are the perfect centerpiece for any milestone birthday or anniversary. Bold, beautiful, and unforgettable!", imagePrompt: 'photorealistic professional photograph of giant metallic gold number balloons on elegant backdrop, surrounded by complementary balloon clusters, studio photography lighting, ultra detailed 8k', tip: 'Surround number balloons with a mini balloon garland for a complete professional look', postType: 'Reel' },
  { topic: 'Halloween Balloon Setup', title: 'Halloween Balloon Decor That Will Scare and WOW', caption: "Get spooky this season! 🎃🕷️ Our Halloween balloon installations are hauntingly beautiful. From office parties to trick-or-treat events — we bring the BOO!", imagePrompt: 'photorealistic professional photograph of dramatic Halloween balloon decoration in black orange purple and green, spider webs pumpkins, moody atmospheric lighting, ultra detailed 8k', tip: 'Combine matte black with chrome orange balloons for a sophisticated Halloween aesthetic', postType: 'Reel' },
  { topic: 'Christmas Balloon Tree', title: 'Forget Regular Trees — THIS Is Christmas Now', caption: "Santa approved! 🎄🎈 Our balloon Christmas trees are the most unique holiday decoration you've ever seen. Perfect for homes, offices, and events. Book early!", imagePrompt: 'photorealistic professional photograph of stunning balloon Christmas tree shape in red green gold and silver balloons, festive living room, fireplace, Christmas morning light, ultra detailed 8k', tip: 'Build your balloon tree on a frame for better shape and longer lasting display', postType: 'Reel' },
  { topic: 'New Year Balloon Drop', title: 'New Year Eve Setup That Goes VIRAL Every Time', caption: "Ring in the New Year in style! 🥂🎆 Our New Year Eve balloon drops and installations make every countdown absolutely magical. Let's make memories!", imagePrompt: 'photorealistic professional photograph of spectacular New Year Eve balloon installation in gold silver and champagne, confetti falling, countdown clock, ultra detailed 8k', tip: 'Fill net drops with a mix of chrome, confetti, and clear balloons for maximum visual impact', postType: 'Reel' },
  { topic: 'Balloon Flower Arrangement', title: 'These Balloon Flowers Look Better Than Real Ones', caption: "Who says flowers are the only option? 🌸🎈 Our balloon flower arrangements last forever and look absolutely stunning. Perfect gift, perfect decor!", imagePrompt: 'photorealistic professional photograph of incredibly detailed balloon flower arrangement in pink white and lavender, resembling real roses and peonies, elegant vase display, studio lighting, ultra detailed 8k', tip: 'Use foil balloons in flower shapes as centerpieces that last way longer than real flowers', postType: 'Reel' },
  { topic: 'Luxury Balloon Box', title: 'The Balloon Gift Box That Breaks The Internet', caption: "Open it and be AMAZED! 🎁💫 Our surprise balloon gift boxes are the ultimate present for any occasion. Imagine the look on their face when it opens!", imagePrompt: 'photorealistic professional photograph of elegant luxury balloon surprise box being opened with colorful helium balloons floating out, confetti burst, pure joy expression, ultra detailed 8k', tip: 'Mix helium balloons with confetti inside the box for the most dramatic reveal moment', postType: 'Reel' },
  { topic: 'Gender Reveal Balloon Pop', title: 'Gender Reveal Moment That Made Everyone CRY', caption: "The most emotional moment of your life deserves the BEST decor! 💙💗 Our gender reveal balloon setups create picture-perfect memories that last a lifetime!", imagePrompt: 'photorealistic professional photograph of magical gender reveal balloon pop with burst of pink confetti and smoke, excited parents and family, outdoor garden setting, golden hour light, ultra detailed 8k', tip: 'Use a large black balloon filled with colored confetti for the most dramatic gender reveal', postType: 'Reel' },
  { topic: 'Balloon Backdrop for Photos', title: 'The Photo Backdrop Everyone Is Talking About', caption: "Give your guests the PERFECT photo op! 📸🎈 Our balloon backdrops are designed to make every photo look stunning. Ideal for events, parties, and brand activations!", imagePrompt: 'photorealistic professional photograph of stunning custom balloon backdrop wall in ombre pastel colors, people taking photos in front, soft studio lighting, ultra detailed 8k', tip: 'Leave the center of your balloon backdrop clear to give guests the best photo framing', postType: 'Reel' },
  { topic: 'Quinceañera Balloon Decor', title: 'Quinceañera Setup Fit For A Princess', caption: "She's been dreaming of this day! 👑🌹 Our Quinceañera balloon decorations combine elegance, color, and tradition into something truly magical. Her special day deserves perfection!", imagePrompt: 'photorealistic professional photograph of breathtaking quinceañera balloon decoration in royal pink purple and gold, tiara theme, grand ballroom, fairy lights, ultra detailed 8k', tip: 'Crown and tiara balloon toppers make Quinceañera setups instantly recognizable and royal', postType: 'Reel' },
  { topic: 'Balloon Delivery Surprise', title: 'Surprise Balloon Delivery That Went VIRAL', caption: "Imagine opening your door to THIS! 🎈😱 Our surprise balloon deliveries are the ultimate way to make someone feel incredibly special. Send happiness today!", imagePrompt: 'photorealistic professional photograph of massive colorful balloon bouquet delivery surprise, recipient with shocked happy expression, bright front door, sunny day, ultra detailed 8k', tip: 'Same-day balloon delivery creates the biggest emotional impact for surprise moments', postType: 'Reel' },
  { topic: 'Table Centerpiece Balloons', title: 'Table Centerpieces That Elevate Your Whole Event', caption: "The details make the event! 🌟🎈 Our balloon table centerpieces are the conversation starter at every table. Affordable luxury for your celebration!", imagePrompt: 'photorealistic professional photograph of elegant balloon table centerpiece arrangement in gold champagne and white, luxury event dinner table setting, ambient lighting, ultra detailed 8k', tip: 'Use weighted balloon centerpieces with different heights for a dynamic table design', postType: 'Reel' },
  { topic: 'Balloon Tunnel Entrance', title: 'Walk Through This Balloon Tunnel and Lose Your Mind', caption: "Make an ENTRANCE that people will talk about! 🚀🎈 Our balloon tunnels transform any party entrance into a magical experience. The wow factor is unmatched!", imagePrompt: 'photorealistic professional photograph of spectacular balloon tunnel corridor in rainbow colors, guests walking through, festive lighting, grand scale installation, ultra detailed 8k', tip: 'Balloon tunnels look best when lit from inside with string lights for an immersive glow', postType: 'Reel' },
  { topic: 'Retirement Party Balloons', title: 'Retirement Party Ideas That Honor Their Journey', caption: "They gave their best — now let's celebrate them PROPERLY! 🏆🎈 Our retirement balloon setups are elegant, personalized, and deeply meaningful. Honor their legacy in style!", imagePrompt: 'photorealistic professional photograph of elegant retirement party balloon decoration in gold silver and navy, years of service milestone display, professional venue, ultra detailed 8k', tip: 'Create a personalized balloon sign with years of service for a meaningful retirement display', postType: 'Reel' },
  { topic: 'Easter Balloon Arrangement', title: 'Easter Balloon Setup That Will Make Kids Scream', caption: "Hoppy Easter to the most adorable decorations! 🐣🌷 Our Easter balloon arrangements bring Spring indoors with the most cheerful colors and designs. Order yours now!", imagePrompt: 'photorealistic professional photograph of adorable Easter balloon arrangement in pastel yellow lavender mint and pink, egg and bunny balloon shapes, bright spring decor, ultra detailed 8k', tip: 'Bunny ear balloon toppers on bouquets are the cutest Easter detail for kids parties', postType: 'Reel' },
  { topic: 'Valentines Heart Balloons', title: "Valentine's Setup So Romantic It's Almost Illegal", caption: "Love is in the air — and the balloons! ❤️🎈 Our Valentine's Day setups create the most romantic atmospheres. Surprise someone special this February!", imagePrompt: 'photorealistic professional photograph of ultra romantic Valentines Day balloon display with red pink and rose gold hearts, floating candles and roses, intimate candlelit atmosphere, ultra detailed 8k', tip: "Heart-shaped foil balloons keep their shape longer than latex — perfect for Valentine's surprises", postType: 'Reel' },
  { topic: 'Tropical Party Balloons', title: 'Tropical Balloon Party That Feels Like Vacation', caption: "Bring the beach to the party! 🌺🌴 Our tropical balloon setups turn any space into a paradise. Perfect for pool parties, luaus, and summer celebrations!", imagePrompt: 'photorealistic professional photograph of vibrant tropical theme balloon decoration in teal coral orange and green, palm leaf and flamingo elements, summer party outdoor setting, ultra detailed 8k', tip: 'Mix leaf foliage with balloons for an organic tropical theme that looks effortlessly festive', postType: 'Reel' },
  { topic: 'Sports Theme Balloons', title: 'Game Day Balloon Setup That Pumps Up The Crowd', caption: "LET'S GO TEAM! 🏆⚽ Our sports themed balloon setups bring the stadium energy to your party. Perfect for watch parties, player celebrations, and championship events!", imagePrompt: 'photorealistic professional photograph of energetic sports celebration balloon decoration in team colors red and blue, football soccer elements, championship trophy display, ultra detailed 8k', tip: "Match your team's exact colors for sports balloon setups — fans will love the attention to detail", postType: 'Reel' },
  { topic: 'Eid Balloon Celebration', title: 'Eid Mubarak Balloon Setup That Is Absolutely Gorgeous', caption: "Eid Mubarak to all celebrating! 🌙⭐ Our Eid balloon setups blend tradition with modern elegance. Create unforgettable memories with family this Eid!", imagePrompt: 'photorealistic professional photograph of magnificent Eid celebration balloon decoration in gold emerald green and royal purple, crescent moon and star balloon shapes, ornate venue, ultra detailed 8k', tip: 'Crescent and star foil balloons are the signature detail for stunning Eid celebrations', postType: 'Reel' },
  { topic: 'Prom Night Balloon Setup', title: 'Prom Entrance Setup That Will Drop Jaws', caption: "Make prom night LEGENDARY! 🌟👑 Our prom balloon setups turn the entrance into a red carpet moment. They'll be talking about this night forever!", imagePrompt: 'photorealistic professional photograph of glamorous prom night balloon arch and columns in royal blue silver and white, red carpet entrance, fairy lights, ultra detailed 8k', tip: 'Tunnel arches at prom entrances create the ultimate grand arrival photo opportunity', postType: 'Reel' },
  { topic: 'Balloon Gift Tower', title: 'The Balloon Tower Gift That Breaks All Records', caption: "Stack it HIGH and watch their eyes go wide! 🎁🎈 Our balloon gift towers are the most impressive way to say congratulations, happy birthday, or I love you!", imagePrompt: 'photorealistic professional photograph of impressive tall balloon gift tower in multi-colored metallic balloons, ribbon cascades, elegant gift box base, studio photography, ultra detailed 8k', tip: 'Balloon towers stay stable longer when you use a weighted base and clear fishing line support', postType: 'Reel' },
  { topic: 'Balloon Sculpture Art', title: 'This Balloon Sculpture Took Our Breath Away', caption: "Balloons are an art form! 🎨🎈 Our custom balloon sculptures bring your wildest ideas to life. From animals to landmarks — if you can dream it, we can balloon it!", imagePrompt: 'photorealistic professional photograph of incredible detailed balloon sculpture art piece of a swan or unicorn, vibrant colors, skilled artisan crafting, exhibition gallery setting, ultra detailed 8k', tip: 'Balloon sculptures last longer when kept away from direct sunlight and sharp surfaces', postType: 'Reel' },
];

const now = new Date();
const dayOfYear = Math.floor((now.getTime() - new Date(now.getFullYear(), 0, 0).getTime()) / 86400000);
const idx = dayOfYear % topics.length;
const t = topics[idx];

const result = {
  topic: t.topic,
  title: t.title,
  caption: t.caption,
  hashtags: HASHTAGS,
  imagePrompt: t.imagePrompt,
  postType: t.postType,
  tip: t.tip
};

// Output in same format as LangChain Anthropic node (json.text field)
return [{ json: { text: JSON.stringify(result) } }];
"""

parse_js_json  = json.dumps(parse_js)
extract_js_json = json.dumps(extract_js)
content_js_json = json.dumps(FREE_CONTENT_JS.strip())

sdk = f"""import {{ workflow, node, trigger }} from '@n8n/workflow-sdk';

const manualTrigger = trigger({{
  type: 'n8n-nodes-base.manualTrigger', version: 1,
  config: {{ name: 'Manual Trigger', id: 'manual-1', position: [0, 352],
    parameters: {{}} }},
  output: [{{}}]
}});

const scheduleTrigger = trigger({{
  type: 'n8n-nodes-base.scheduleTrigger', version: 1.1,
  config: {{ name: 'Every Day 9AM', id: 'sched-1', position: [0, 160],
    parameters: {{ rule: {{ interval: [{{ field: 'cronExpression', expression: '0 9 * * *' }}] }} }} }},
  output: [{{}}]
}});

const generateContent = node({{
  type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Generate Trending Content', id: 'gen-content', position: [240, 256],
    parameters: {{ jsCode: {content_js_json} }} }},
  output: [{{}}]
}});

const parseRow = node({{
  type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Parse & Build Row', id: 'parse-row', position: [480, 256],
    parameters: {{ jsCode: {parse_js_json} }} }},
  output: [{{}}]
}});

const downloadImage = node({{
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: {{ name: 'Download Reel Image', id: 'dl-img', position: [720, 256],
    parameters: {{
      url: '={{{{ $json.imageUrl }}}}',
      options: {{ response: {{ response: {{ responseFormat: 'file', outputPropertyName: 'imageData' }} }}, timeout: 120000 }}
    }}
  }},
  output: [{{}}]
}});

const uploadCatbox = node({{
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: {{ name: 'Upload to Catbox', id: 'upload-catbox', position: [960, 192],
    parameters: {{
      method: 'POST',
      url: 'https://litterbox.catbox.moe/resources/internals/api.php',
      sendBody: true,
      contentType: 'multipart-form-data',
      bodyParameters: {{ parameters: [
        {{ name: 'reqtype', value: 'fileupload' }},
        {{ name: 'time', value: '72h' }},
        {{ parameterType: 'formBinaryData', name: 'fileToUpload', inputDataFieldName: 'imageData' }}
      ] }},
      options: {{ response: {{ response: {{ responseFormat: 'text' }} }} }}
    }}
  }},
  output: [{{}}]
}});

const saveImageDrive = node({{
  type: 'n8n-nodes-base.googleDrive', version: 3,
  config: {{ name: 'Save Image to Drive', id: 'save-img', position: [960, 352],
    parameters: {{
      operation: 'upload',
      inputDataFieldName: 'imageData',
      name: "={{ $('Parse & Build Row').item.json.Topic + ' - ' + $('Parse & Build Row').item.json.Date + '.jpg' }}",
      driveId: {{ '__rl': true, mode: 'list', value: 'My Drive' }},
      folderId: {{ '__rl': true, value: '1gxbenDHHzUIxW4JqSc2h8_44hO2iPEwe', mode: 'list', cachedResultName: 'MY CONTENT' }},
      options: {{}}
    }}
  }},
  output: [{{}}]
}});

const createRender = node({{
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: {{ name: 'Create Shotstack Render', id: 'create-render', position: [1200, 192],
    parameters: {{
      method: 'POST',
      url: 'https://api.shotstack.io/v1/render',
      sendHeaders: true,
      headerParameters: {{ parameters: [
        {{ name: 'x-api-key', value: '71bXjUcRMKS2yEp2ZEDXfTC0TPychF6cQ4aUuOjb' }},
        {{ name: 'Content-Type', value: 'application/json' }}
      ] }},
      sendBody: true, contentType: 'raw',
      body: "={{ JSON.stringify({{ timeline: {{ background: '#000000', tracks: [{{ clips: [{{ asset: {{ type: 'image', src: $json.data }}, start: 0, length: 5, effect: 'zoomIn' }}] }}] }}, output: {{ format: 'mp4', resolution: 'hd', aspectRatio: '9:16' }} }}) }}",
      options: {{}}
    }}
  }},
  output: [{{}}]
}});

const waitRender = node({{
  type: 'n8n-nodes-base.wait', version: 1.1,
  config: {{ name: 'Wait for Render', id: 'wait-render', position: [1440, 192],
    parameters: {{ amount: 180 }} }},
  output: [{{}}]
}});

const getRender = node({{
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: {{ name: 'Get Shotstack Render', id: 'get-render', position: [1680, 192],
    parameters: {{
      url: "=https://api.shotstack.io/v1/render/{{{{ $('Create Shotstack Render').item.json.response.id }}}}",
      sendHeaders: true,
      headerParameters: {{ parameters: [
        {{ name: 'x-api-key', value: '71bXjUcRMKS2yEp2ZEDXfTC0TPychF6cQ4aUuOjb' }}
      ] }},
      options: {{}}
    }}
  }},
  output: [{{}}]
}});

const extractUrl = node({{
  type: 'n8n-nodes-base.code', version: 2,
  config: {{ name: 'Extract Video URL', id: 'extract-url', position: [1920, 192],
    parameters: {{ jsCode: {extract_js_json} }} }},
  output: [{{}}]
}});

const downloadVideo = node({{
  type: 'n8n-nodes-base.httpRequest', version: 4.2,
  config: {{ name: 'Download Video', id: 'dl-video', position: [2160, 192],
    parameters: {{
      url: '={{{{ $json.videoUrl }}}}',
      options: {{ response: {{ response: {{ responseFormat: 'file', outputPropertyName: 'videoData' }} }}, timeout: 120000 }}
    }}
  }},
  output: [{{}}]
}});

const saveVideoDrive = node({{
  type: 'n8n-nodes-base.googleDrive', version: 3,
  config: {{ name: 'Save Video to Drive', id: 'save-video', position: [2400, 192],
    parameters: {{
      operation: 'upload',
      inputDataFieldName: 'videoData',
      name: "={{ $('Parse & Build Row').item.json.Topic + ' - ' + $('Parse & Build Row').item.json.Date + '.mp4' }}",
      driveId: {{ '__rl': true, mode: 'list', value: 'My Drive' }},
      folderId: {{ '__rl': true, value: '1QSAOTPFBIg-kYlnSg3mchq2VU0cvFFb8', mode: 'list', cachedResultName: 'CONTENT VIDEO' }},
      options: {{}}
    }}
  }},
  output: [{{}}]
}});

export default workflow('{WORKFLOW_ID}', 'Daily Reel Creator - Country Cove Balloons')
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
print('Done! ' + str(res)[:200] if res else 'ERROR: update returned None')
