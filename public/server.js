const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const querystring = require('querystring');
const { handleFormSubmission, generateAnalysisEmail } = require('./form-handler');

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
    
    // Handle form submission
    if (req.method === 'POST' && parsedUrl.pathname === '/submit-form') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        
        req.on('end', () => {
            try {
                const formData = querystring.parse(body);
                const lead = handleFormSubmission(formData);
                const emailContent = generateAnalysisEmail(formData);
                
                // Save email to file for manual sending
                const emailFile = path.join(__dirname, `email-${lead.id}.json`);
                fs.writeFileSync(emailFile, JSON.stringify(emailContent, null, 2));
                
                // Redirect to thank you page with parameters
                const redirectUrl = `/thank-you.html?firstName=${encodeURIComponent(formData.firstName || '')}&company=${encodeURIComponent(formData.company || '')}`;
                res.writeHead(302, { 'Location': redirectUrl });
                res.end();
                
                console.log(`New lead: ${formData.firstName} from ${formData.company}`);
                console.log(`Email template saved: email-${lead.id}.json`);
            } catch (error) {
                console.error('Form submission error:', error);
                res.writeHead(500, { 'Content-Type': 'text/html' });
                res.end('<h1>Error processing form</h1><p>Please try again.</p>');
            }
        });
        return;
    }
    
    // Handle free-trial.html specifically
    if (req.url === '/free-trial' || req.url === '/free-trial.html') {
        filePath = path.join(__dirname, 'free-trial.html');
    }
    
    const extname = path.extname(filePath);
    let contentType = 'text/html';
    
    switch (extname) {
        case '.css':
            contentType = 'text/css';
            break;
        case '.js':
            contentType = 'text/javascript';
            break;
        case '.json':
            contentType = 'application/json';
            break;
        case '.png':
            contentType = 'image/png';
            break;
        case '.jpg':
        case '.jpeg':
            contentType = 'image/jpeg';
            break;
    }
    
    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end('<h1>404 Not Found</h1><p>File not found: ' + req.url + '</p>');
            } else {
                res.writeHead(500);
                res.end('Server Error: ' + err.code);
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        }
    });
});

const PORT = 8080;
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log(`Free trial page: http://localhost:${PORT}/free-trial.html`);
});
