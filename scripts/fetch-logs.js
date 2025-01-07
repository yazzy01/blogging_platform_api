const https = require('https');

const API_KEY = 'rnd_vyYAMW5gSwKBOvG9MrWn8FWBUCPW';
const SERVICE_ID = 'srv-cts1h65umphs73fitqj0';

const options = {
  hostname: 'api.render.com',
  path: `/v1/services/${SERVICE_ID}/logs`,
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  }
};

console.log('Fetching deployment logs...');

const req = https.request(options, (res) => {
  let data = '';
  
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    try {
      const logs = JSON.parse(data);
      if (Array.isArray(logs)) {
        logs.forEach(log => {
          const timestamp = new Date(log.timestamp).toLocaleString();
          console.log(`[${timestamp}] ${log.message}`);
        });
      } else {
        console.log('Raw response:', data);
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
