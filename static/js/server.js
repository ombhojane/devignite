const express = require('express');
const app = express();
const path = require('path');

app.use(express.static('res/register'));
app.use(express.static('res/home'));
app.use(express.static('res/map'));
app.use(express.static('res/bookslot'));
app.use(express.urlencoded({ extended: true }));

// Define route to serve the JSON file
app.get('/data', (req, res) => {
    // Construct the absolute path to the JSON file
    const filePath = path.join(__dirname, 'evCharger.json');
    res.sendFile(filePath);
});

app.get('/bookSlot', (req, res) => {
    res.sendFile(path.join(__dirname, 'res/bookslot/bookSlot.html'));
})

app.get('/mumbai', (req, res) => {
    const filePath = path.join(__dirname, 'mumbai.json');
    res.sendFile(filePath);
})

app.get('/pune', (req, res) => {
    const filePath = path.join(__dirname, 'pune.json');
    res.sendFile(filePath);
})

app.post('/bookSlot', (req, res) => {
    res.redirect('/bookSlot')
})

app.get('/map', (req, res) => {
    // Construct the absolute path to the JSON file
    res.sendFile(path.join(__dirname, 'res/map/map.html'));
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'res/register/register.html'));
});

app.get('/home', (req, res) => {
    res.sendFile(path.join(__dirname, 'res/home/home.html'));
});

app.post('/registerEVBranch', (req, res) => {
    // Handle form submission
    res.send('Received the data successfully!');
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
