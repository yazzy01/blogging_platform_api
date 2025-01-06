const https = require('https');

const API_KEY = 'rnd_vyYAMW5gSwKBOvG9MrWn8FWBUCPW';
const SERVICE_ID = 'srv-cts1h65umphs73fitqj0';
const DEPLOY_ID = 'dep-ctu6k8tds78s73flf3d0';

const options = {
  hostname: 'api.render.com',
  path: `/v1/services/${SERVICE_ID}/deploys/${DEPLOY_ID}`,
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  }
};

console.log('Checking deployment status...');

const req = https.request(options, (res) => {
  let data = '';
  
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    try {
      const deploy = JSON.parse(data);
      console.log('\nDeployment Status:', deploy.status);
      if (deploy.finishedAt) {
        console.log('Finished at:', new Date(deploy.finishedAt).toLocaleString());
      }
    } catch (e) {
      console.log('Raw response:', data);
    }
  });
});

req.on('error', (error) => {
  console.error('Error:', error);
});

req.end();
