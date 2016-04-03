//load required modules
var http = require("http");
const child_process = require('child_process');

//use http instance to create server, bind to port 8081
http.createServer(function (request, response) {

   // HTTP Status: 200 : OK
   // Content Type: text/plain
   response.writeHead(200, {'Content-Type': 'text/plain'});

   // Response Body
   response.end('Hello World\n');
}).listen(8081);

// Console will print the message
console.log('Server running at http://127.0.0.1:8081/');

//Run python script and print results
child_process.exec('python vid_moderator.py test_video_files/birds.mp4 AIzaSyCPZJ3_hlLTcdMtkBEzXHXIuGkmNn1TeFc',vidModeratorCB)

//vid_moderator.py callback function
function vidModeratorCB(error, stdout, stderr) {
    if (error) console.error(error);
    else console.log(stdout);
}
