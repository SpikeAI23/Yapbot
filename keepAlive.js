// Import the express module to create the server
const express = require('express');
const app = express();

// Serve a simple response to any incoming request to keep the bot alive
app.get('/', (req, res) => {
  res.send('Bot is alive!');
});

// Start the server on port 3000
app.listen(3000, () => {
  console.log('Keep-alive server is running on port 3000!');
});