module.exports = {
    name: "ping",
    description: "Replies with Pong!",
    async execute(interaction) {
      // Respond with "Pong!" and include the bot's response time
      const sent = await interaction.reply({ content: "Pong!", fetchReply: true });
      const timeDifference = sent.createdTimestamp - interaction.createdTimestamp;
      interaction.editReply(`Pong! 🏓 Latency is ${timeDifference}ms.`);
    },
  };
  