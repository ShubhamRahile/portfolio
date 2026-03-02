const fs = require('fs');
const path = require('path');

// Create deployment directory
const deployDir = './docs';
if (!fs.existsSync(deployDir)) {
    fs.mkdirSync(deployDir);
}

// Files to copy for GitHub Pages
const filesToCopy = [
    'index.html',
    'style.css',
    'script.js',
    'server.js',
    'package.json',
    '.env',
    'Shubham.jpeg',
    'Shubham Rahile CV.pdf'
];

// Copy files
filesToCopy.forEach(file => {
    if (fs.existsSync(file)) {
        const source = fs.readFileSync(file);
        fs.writeFileSync(path.join(deployDir, file), source);
        console.log(`✓ Copied ${file}`);
    }
});

// Create a simple GitHub Pages compatible server.js
const ghPagesServer = `
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files
app.use(express.static(path.join(__dirname, '.')));

// Serve index.html for all routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(\`Server running on port \${PORT}\`);
});
`;

fs.writeFileSync(path.join(deployDir, 'gh-pages-server.js'), ghPagesServer);

console.log('\n✅ Deployment files created in /docs folder');
console.log('Now follow these steps:');
console.log('1. git init');
console.log('2. git add .');
console.log('3. git commit -m "Initial commit"');
console.log('4. git remote add origin https://github.com/yourusername/portfolio.git');
console.log('5. git push -u origin main');