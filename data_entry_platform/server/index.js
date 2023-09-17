const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 5000;

// Middlewares
app.use(cors());
app.use(bodyParser.json());

app.post('/submit', (req, res) => {
    const data = req.body;

    // Ensure the data directory exists
    const dataDir = path.join(__dirname, 'data');
    if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir);
    }

    // Get all files for the current rating
    const files = fs.readdirSync(dataDir);
    const ratingFiles = files.filter(file => file.startsWith(data.rating) && file.includes(`.json`));

    // Extract count numbers and find the latest count
    const counts = ratingFiles.map(file => parseInt(file.split('-')[1]));
    const latestCount = counts.length ? Math.max(...counts) : 0;

    // Generate the filename using the next count number
    const filename = `${data.rating}-${latestCount + 1}.json`;

    // Save data to the generated filename inside the data directory
    fs.writeFileSync(path.join(dataDir, filename), JSON.stringify(data, null, 2));

    res.json({ message: 'Data saved successfully!' });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
