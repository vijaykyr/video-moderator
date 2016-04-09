/*
 * Author: reddyv@
 * Last Updated: 04-07-2016
 * Usage: node express_server.js
 * ToDo:
 *  1) Add form validation
 *
*/

//load required modules
var express = require('express'); //npm module: web framework
var multer = require('multer'); //npm module: parses multipart form data
var fs = require('fs');
const child_process = require('child_process');

//initialize
var express = express();
var upload = multer({ dest: __dirname, limits: {fileSize: 1e8} }); //limit file size to 100MB to prevent DoS

//define routes
express.get('/', function (req, res) {
  res.sendFile(__dirname + '/html/form.html'); //__dirname is a nodejs global representing the current directory
});

express.post('/', upload.single('video_file'), function (req, res) {
  //asynchronously call python vid_moderator
  child_process.exec('python vid_moderator.py ' + req.file.path + ' ' + req.body.api_key
    + ' --sample-rate=' + req.body.sample_rate + ' --response-type=' + req.body.response_type,
        function (error, stdout, stderr) {
            if (error) console.error(error);
            else {
               res.send(stdout);
               //cleanup
               fs.unlinkSync(req.file.path)
            }

        })

  console.log('processing');
});

//listen
express.listen(80, function () {
  console.log('Express server running on port 80');
});

