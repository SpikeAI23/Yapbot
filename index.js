const { Client, GatewayIntentBits, Collection } = require('discord.js');
const fs = require('fs');
const path = require('path');
const { REST, Routes } = require('discord.js');
require('dotenv').config(); // Load environment variables

const client = new Client({ intents: [GatewayIntentBits.Guilds] });
client.commands = new Collection();
const commandsPath = path.join(__dirname, 'commands');

// Function to load commands
function loadCommands() {
  client.commands.clear();
  const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

  for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    delete require.cache[require.resolve(filePath)]; // Clear the require cache
    const command = require(filePath);
    client.commands.set(command.name, command);
  }

  console.log('Commands loaded:', [...client.commands.keys()]);
}

// Function to deploy commands
async function deployCommands() {
  const commands = [];
  client.commands.forEach(command => {
    commands.push({
      name: command.name,
      description: command.description,
    });
  });

  const rest = new REST({ version: '10' }).setToken(process.env.TOKEN);

  try {
    console.log('Deploying application (/) commands...');
    await rest.put(Routes.applicationCommands(process.env.CLIENT_ID), { body: commands });
    console.log('Successfully deployed application (/) commands.');
  } catch (error) {
    console.error('Error deploying commands:', error);
  }
}

// Watch for changes in the commands folder
fs.watch(commandsPath, (eventType, filename) => {
  if (filename && filename.endsWith('.js')) {
    console.log(`Detected changes in ${filename}. Reloading commands...`);
    loadCommands();
    deployCommands();
  }
});

// Event: Bot ready
client.once('ready', async () => {
  console.log(`Logged in as ${client.user.tag}`);
  loadCommands();
  await deployCommands();
});

// Event: Interaction create
client.on('interactionCreate', async interaction => {
  if (!interaction.isCommand()) return;

  const command = client.commands.get(interaction.commandName);
  if (!command) return;

  try {
    await command.execute(interaction);
  } catch (error) {
    console.error(error);
    await interaction.reply({ content: 'There was an error executing this command.', ephemeral: true });
  }
});

// Login to Discord using token from .env
client.login(process.env.TOKEN);
