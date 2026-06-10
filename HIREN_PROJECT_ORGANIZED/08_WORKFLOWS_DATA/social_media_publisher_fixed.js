import { workflow, node, trigger } from '@n8n/workflow-sdk';

const FACEBOOK_TOKEN = 'EAAOM95s8ZCigBRc1UO7M5wxmiSotgsQ17atYz324ZCJ9XUX0IHorsMq5ot7eH755WNXbkeWAYA5njlChG4sauGeQ9zzkLscfIUKg9sjRN6Rgg5E1eXZBWNchrdYZCzyee4lSPNG8id7v4f93OolgDpesAQhAZADONzcZAPzViZCwJA9ZBXrmAT3qiMQNcPXCnginm3FwmVoeZB569DU5Ku4fJJF920kdpUzE0SmQaKdihvQYZD';
const WHATSAPP_TOKEN = 'EAAOM95s8ZCigBRXBn5ZBpBTJQVlZAoSW2Bylmq8ZAHXZAteKQwnqAKCy5Atd1ui3kZB8Hy5ScF7gF2kuAdisXsO8HZAXZCMn1abLZBK7ZAKuiREdEoZAI031HIqKjL72lQi6nsHM5eS7wRhveQZASSj69ODIRyhoy6GqkHVntHGvOyla3CUZBgEf8SiLe5FV4JYR5kyUURJTDBMRZCpGDdxtDysM0D2mVP26AllxbV4y9TY2ArtWz2iYZB2hqKXpTlxhVpGgfZCIgWxCWMlHbzj1x8cKYKZBA8yBx';

const scheduleTrigger = trigger({
  type: 'n8n-nodes-base.scheduleTrigger',
  version: 1.1,
  config: {
    name: 'Every Day 11PM',
    parameters: {
      rule: { interval: [{ field: 'cronExpression', expression: '0 23 * * *' }] }
    },
    position: [0, 192]
  },
  output: [{}]
});

const getLatestVideo = node({
  type: 'n8n-nodes-base.googleDrive',
  version: 3,
  config: {
    name: 'Get Latest Video from Drive',
    parameters: {
      resource: 'fileFolder',
      operation: 'search',
      queryFilters: {
        values: [
          {
            field: 'parents',
            operator: 'in',
            value: '1QSAOTPFBIg-kYlnSg3mchq2VU0cvFFb8'
          }
        ]
      },
      returnAll: false,
      limit: 1,
      options: {
        fields: ['*'],
        orderBy: 'modifiedTime desc'
      }
    },
    position: [224, 192]
  },
  output: [{ id: 'abc123', name: 'birthday-balloon.mp4', webViewLink: 'https://drive.google.com', modifiedTime: '2026-05-20T10:00:00Z' }]
});

const generateContent = node({
  type: '@n8n/n8n-nodes-langchain.anthropic',
  version: 1,
  config: {
    name: 'Generate Viral Post Content',
    parameters: {
      modelId: { __rl: true, value: 'claude-sonnet-4-6', mode: 'list', cachedResultName: 'claude-sonnet-4-6' },
      messages: {
        values: [{
          content: "=Today is {{ $now.toFormat('MMMM d, yyyy') }}. You are a viral social media expert for Country Cove Balloons, a luxury US balloon decoration business.\n\nToday's video topic is: \"{{ $json.name.replace(/\\.(mp4|mov|avi|mp4)$/i, '').split(' - ')[0] }}\"\n\nCreate a VIRAL, emotionally compelling post for Facebook, Facebook Group, and WhatsApp.\n\nReturn ONLY raw JSON with no markdown:\n{\"title\":\"catchy viral title under 10 words with emojis\",\"caption\":\"3-4 sentence emotional caption with storytelling, strong call to action, and relevant emojis.\",\"hashtags\":\"#balloon #balloonart #balloondecorations #birthdayballoons #partyballoons #balloonbouquet #eventdecor #balloondesign #balloonartist #partydecor #celebrationballoons #balloonlove #countrycoveballoons #balloonbusiness #partyplanning #weddingdecor #babyshower #balloongarland #luxurydecor #ballooninstallation #partyinspo #eventplanner #balloondelivery #balloontrends #balloonwall #organicballoons #luxuryevents #partygoals #ballooninspiration #handmade\"}"
        }]
      },
      options: {}
    },
    position: [448, 192]
  },
  output: [{ text: '{"title":"🎈 Magical Moments That Last Forever!","caption":"Every celebration deserves magic.","hashtags":"#balloon"}' }]
});

const buildPostData = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Build Post Data1',
    parameters: {
      jsCode: `const raw = $input.first().json.text || ($input.first().json.content?.[0]?.text);
const match = raw.match(/\\{[\\s\\S]*\\}/);
if (!match) throw new Error('No JSON from Claude: ' + raw.substring(0, 300));
const ai = JSON.parse(match[0]);

const file = $('Get Latest Video from Drive').item.json;
if (!file || !file.id) throw new Error('No video found in CONTENT VIDEO folder! Drive returned: ' + JSON.stringify(file).substring(0, 200));

const nameNoExt = (file.name || '').replace(/\\.(mp4|mov|avi|mkv|webm)$/i, '');
const topic = nameNoExt.split(' - ')[0] || nameNoExt;
const postText = ai.title + '\\n\\n' + ai.caption + '\\n\\n' + ai.hashtags;

return [{ json: {
  fileId: file.id,
  filename: file.name,
  topic: topic,
  Title: ai.title,
  Caption: ai.caption,
  Hashtags: ai.hashtags,
  postText: postText
} }];`
    },
    position: [672, 192]
  },
  output: [{ fileId: 'abc123', filename: 'birthday-balloon.mp4', topic: 'birthday-balloon', Title: '🎈 Magical Moments!', Caption: 'Every celebration...', Hashtags: '#balloon', postText: '🎈 Magical Moments!\n\nEvery celebration...\n\n#balloon' }]
});

const downloadVideo = node({
  type: 'n8n-nodes-base.googleDrive',
  version: 3,
  config: {
    name: 'Download Video from Drive',
    parameters: {
      operation: 'download',
      fileId: { __rl: true, value: '={{ $json.fileId }}', mode: 'id' },
      options: { binaryPropertyName: 'videoData' }
    },
    position: [896, 192]
  },
  output: [{}]
});

const uploadToHost = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.2,
  config: {
    name: 'Upload to Public Host',
    parameters: {
      method: 'POST',
      url: 'https://litterbox.catbox.moe/resources/internals/api.php',
      sendBody: true,
      contentType: 'multipart-form-data',
      bodyParameters: {
        parameters: [
          { parameterType: 'formBinaryData', name: 'fileToUpload', inputDataFieldName: 'videoData' },
          { parameterType: 'formData', name: 'reqtype', value: 'fileupload' },
          { parameterType: 'formData', name: 'time', value: '72h' }
        ]
      },
      options: {
        response: {
          response: { responseFormat: 'text', outputPropertyName: 'publicUrl' }
        }
      }
    },
    position: [1120, 192]
  },
  output: [{ publicUrl: 'https://files.catbox.moe/abc123.mp4' }]
});

// FIX: Updated from deprecated v19.0 to v21.0
const postToFacebook = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.2,
  config: {
    name: 'Post to Facebook',
    parameters: {
      method: 'POST',
      url: 'https://graph.facebook.com/v21.0/1074426259093321/videos',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'Content-Type', value: 'application/json' }]
      },
      sendBody: true,
      bodyParameters: {
        parameters: [
          { name: 'file_url', value: "={{ $('Upload to Public Host').item.json.publicUrl }}" },
          { name: 'description', value: "={{ $('Build Post Data1').item.json.postText }}" },
          { name: 'title', value: "={{ $('Build Post Data1').item.json.Title }}" },
          { name: 'access_token', value: FACEBOOK_TOKEN }
        ]
      },
      options: {}
    },
    position: [1344, 0]
  },
  output: [{ id: '123456789' }]
});

// FIX: Updated from deprecated v19.0 to v21.0
const postToFacebookGroup = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.2,
  config: {
    name: 'Post to Facebook Group1',
    parameters: {
      method: 'POST',
      url: 'https://graph.facebook.com/v21.0/823691467128755/feed',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'Content-Type', value: 'application/json' }]
      },
      sendBody: true,
      contentType: 'json',
      specifyBody: 'keypair',
      bodyParameters: {
        parameters: [
          { name: 'message', value: "={{ $('Build Post Data1').item.json.postText + '\\n\\n Watch: ' + $('Upload to Public Host').item.json.publicUrl }}" },
          { name: 'access_token', value: FACEBOOK_TOKEN }
        ]
      },
      options: {}
    },
    position: [1344, 192]
  },
  output: [{ id: '987654321' }]
});

// FIX: Updated from deprecated v19.0 to v21.0
const postToWhatsApp = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.2,
  config: {
    name: 'Post to WhatsApp',
    parameters: {
      method: 'POST',
      url: 'https://graph.facebook.com/v21.0/1155201714335421/messages',
      sendHeaders: true,
      headerParameters: {
        parameters: [
          { name: 'Authorization', value: `Bearer ${WHATSAPP_TOKEN}` },
          { name: 'Content-Type', value: 'application/json' }
        ]
      },
      sendBody: true,
      contentType: 'json',
      specifyBody: 'keypair',
      bodyParameters: {
        parameters: [
          { name: 'messaging_product', value: 'whatsapp' },
          { name: 'to', value: '918130711383' },
          { name: 'type', value: 'video' },
          { name: 'video', value: "={{ { link: $('Upload to Public Host').item.json.publicUrl, caption: $('Build Post Data1').item.json.postText.substring(0, 1024) } }}" }
        ]
      },
      options: {}
    },
    position: [1344, 384]
  },
  output: [{ messages: [{ id: 'wamid.abc123' }] }]
});

export default workflow('4OxWM0mwiADOCAb8', 'Social Media Publisher - Country Cove Balloons')
  .add(scheduleTrigger)
  .to(getLatestVideo)
  .to(generateContent)
  .to(buildPostData)
  .to(downloadVideo)
  .to(uploadToHost)
  .to(postToFacebook)
  .add(uploadToHost)
  .to(postToFacebookGroup)
  .add(uploadToHost)
  .to(postToWhatsApp);
