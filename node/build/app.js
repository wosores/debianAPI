const http = require('http');

const hostname = '0.0.0.0';
const port = 3000;
const version = process.env.VERSION;

const server = http.createServer((req, res) => {
	res.statusCode = 200;
	res.setHeader('Content-Type', 'text/plain');
	res.end(`Gloria a Deus! ${hostname}:${port}/ and version ${version}`);
});

server.listen(port, hostname, () => {
	console.log(`Server running at http://${hostname}:${port}/`);
});

process.on('SIGINT', function() {
	process.exit();
});
