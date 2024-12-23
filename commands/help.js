const { EmbedBuilder } = require('discord.js');
const fs = require('fs');
const path = require('path');

module.exports = {
  name: "help",
  description: "Displays help information.",
  execute(interaction) {
    // Load all commands
    const commandsPath = path.join(__dirname, '../');
    const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

    // Generate fields for embed
    const commandList = commandFiles.map(file => {
      const command = require(path.join(commandsPath, file));
      return `**/${command.name}**: ${command.description}`;
    }).join('\n');

    // Create embed
    const helpEmbed = new EmbedBuilder()
      .setColor(0x00ffcc)
      .setTitle("Help Menu")
      .setDescription("Here are all the available commands:")
      .addFields({ name: "Commands", value: commandList })
      .setImage("https://example.com/banner.png") // Replace with a URL to your banner image
      .setFooter({ text: "Need more help? Contact the admin!" });

    // Send embed
    interaction.reply({ embeds: [helpEmbed] });
  },
};
