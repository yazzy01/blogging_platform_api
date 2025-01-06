const https = require('https');

const API_KEY = 'rnd_vyYAMW5gSwKBOvG9MrWn8FWBUCPW';
const SERVICE_ID = 'srv-cts1h65umphs73fitqj0';

// Trigger the deploy
const deployOptions = {
  hostname: 'api.render.com',
  path: `/v1/services/${SERVICE_ID}/deploys`,
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  }
};

console.log('Triggering deploy...');

const deployReq = https.request(deployOptions, (deployRes) => {
  console.log(`Deploy Status Code: ${deployRes.statusCode}`);
  
  let deployData = '';
  deployRes.on('data', (chunk) => {
    deployData += chunk;
  });
  
  deployRes.on('end', () => {
    try {
      const response = JSON.parse(deployData);
      console.log('Deploy initiated:', response);
    } catch (e) {
      console.log('Raw response:', deployData);
    }
  });
});

deployReq.on('error', (error) => {
  console.error('Deploy error:', error);
});

deployReq.end();
