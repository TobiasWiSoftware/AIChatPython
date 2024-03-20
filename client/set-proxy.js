const fs = require('fs');
const packageJsonPath = './package.json';

// Lese package.json
let packageJson = require(packageJsonPath);

// Setze den Proxy basierend auf einer Umgebungsvariable
if (process.env.RUNNING_IN_DOCKER === 'true') {
    packageJson.proxy = 'http://python_server:5000';
} else {
    packageJson.proxy = 'http://127.0.0.1:5000';
}

// Schreibe die geänderte package.json zurück
fs.writeFile(packageJsonPath, JSON.stringify(packageJson, null, 2), function (err) {
  if (err) return console.log(err);
  console.log('Proxy wurde in package.json gesetzt.');
});
