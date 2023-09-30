const https = require('https');
const fs = require('fs');
const httpProxy = require('http-proxy');

// Paths to your localhost certificates
const privateKey = fs.readFileSync('./ui.local.key', 'utf8');
const certificate = fs.readFileSync('./ui.local.crt', 'utf8');

const credentials = { key: privateKey, cert: certificate };

// Create an HTTPS service that proxies to the original Next.js dev server
const proxyServer = httpProxy.createProxyServer({
    target: 'http://localhost:3001',
    secure: true // This ensures that the proxy will accept the self-signed certificate
});

// Error handling for the proxy
proxyServer.on('error', (err, req, res) => {
    console.error('Proxy error:', err);
    res.writeHead(500, {
        'Content-Type': 'text/plain'
    });
    res.end('Proxy encountered an error.');
});

https.createServer(credentials, (req, res) => {
    proxyServer.web(req, res);
}).listen(3000, () => {
    console.log('> Proxying https://localhost:3000 to http://localhost:3001');
});
