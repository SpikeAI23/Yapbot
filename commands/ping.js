module.exports = {
    name: 'ping',          // Command name
    description: 'Replies with Pong!',  // Command description
    async execute(interaction) {
      await interaction.reply('Pong!');
    },
  };
  