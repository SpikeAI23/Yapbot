const { REST, Routes } = require('discord.js');
const fs = require('fs');
const path = require('path');
const chokidar = require('chokidar');
require('dotenv').config();

const commands = [];
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

// Load initial commands
const loadCommands = () => {
  commands.length = 0; // Clear previous commands
  const files = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

  files.forEach(file => {
    const command = require(path.join(commandsPath, file));
    commands.push({
      name: command.name,
      description: command.description,
    });
  });
  console.log('Commands loaded:', commands);
};

// Initialize REST client for API requests
const rest = new REST({ version: '10' }).setToken(process.env.TOKEN);

// Function to deploy commands to Discord
const deployCommands = async () => {
  try {
    console.log('Started refreshing application (/) commands.');
    await rest.put(Routes.applicationCommands(process.env.CLIENT_ID), { body: commands });
    console.log('Successfully reloaded application (/) commands.');
  } catch (error) {
    console.error('Error deploying commands:', error);
  }
};

// Watch for changes in the commands folder
const watcher = chokidar.watch(commandsPath, { persistent: true });

watcher.on('change', (filePath) => {
  console.log(`Detected change in file: ${filePath}. Reloading commands...`);
  loadCommands();
  deployCommands();
});

watcher.on('add', (filePath) => {
  console.log(`Detected new file: ${filePath}. Adding to commands...`);
  loadCommands();
  deployCommands();
});

watcher.on('unlink', (filePath) => {
  console.log(`Detected file deletion: ${filePath}. Removing from commands...`);
  loadCommands();
  deployCommands();
});

// Initial load and deploy of commands
loadCommands();
deployCommands();
