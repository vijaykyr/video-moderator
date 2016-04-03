//load required modules
var http = require("http");
var qs = require('querystring');
var fs = require('fs');
const child_process = require('child_process');


//initialize
var form = fs.readFileSync('html/form.html');

//create server, bind to port 8081
http.createServer(function (request, response) {
    if(request.method === "GET") {
      response.writeHead(200, {'Content-Type': 'text/html'});
      response.end(form);
    }
    else if(request.method === "POST") {
      var requestBody = '';
      request.on('data', function(data) {
        requestBody += data;
        if(requestBody.length > 1e6) {
          response.writeHead(413, 'Request Entity Too Large', {'Content-Type': 'text/plain'});
          response.end('413: Request Entity Too Large');
        }
      });
      request.on('end', function() {
        console.log(requestBody);
        var formData = qs.parse(requestBody);
        response.writeHead(200, {'Content-Type': 'text/html'});
        response.write('<!doctype html><html><head><title>response</title></head><body>');
        response.write('Thanks for the data!<br />User Name: '+formData.UserName);
        response.write('<br />Repository Name: '+formData.Repository);
        response.write('<br />Branch: '+formData.Branch);
        response.end('</body></html>');
      });
    }
}).listen(8081);

// Console will print the message
console.log('Server running at http://127.0.0.1:8081/');

//Run python script and print results
//child_process.exec('python vid_moderator.py test_video_files/birds.mp4 AIzaSyCPZJ3_hlLTcdMtkBEzXHXIuGkmNn1TeFc',vidModeratorCB)

//vid_moderator.py callback function
function vidModeratorCB(error, stdout, stderr) {
    if (error) console.error(error);
    else console.log(stdout);
}
