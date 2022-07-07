const express = require("express");
const { spawn } = require('child_process');
require("dotenv").config()
const fs = require('fs');

const app = express();

app.use(express.json());

app.get('/', async (req, res) => {
    var fileName;
    // spawn new child process to call the python script
    const python = spawn('python', ['bloodStoneV2.py']);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        fileName = data.toString().replace(/(\r\n|\n|\r)/gm, "");
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        let rawdata = fs.readFileSync(`${fileName}.json`);
        let student = JSON.parse(rawdata);
        res.send(student)
    });
})

app.listen(process.env.PORT, (req, res) => {
    console.log("Server Online 🚀 on port ", process.env.PORT)
})