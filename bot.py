import discord
from discord.ext import commands, tasks
import asyncio
import random
from datetime import datetime
import os
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot Ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Event: Member Join
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}!")

# Event: Member Leave
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"Goodbye, {member.mention}. We'll miss you!")

# Event: Message Edit
@bot.event
async def on_message_edit(before, after):
    channel = before.channel
    await channel.send(f"Message edited:
Before: {before.content}
After: {after.content}")

# Event: Message Delete
@bot.event
async def on_message_delete(message):
    channel = message.channel
    await channel.send(f"Message deleted: {message.content}")

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# Command: Roll Dice
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, sides = map(int, dice.split('d'))
        results = [random.randint(1, sides) for _ in range(rolls)]
        await ctx.send(f'Results: {results} | Total: {sum(results)}')
    except ValueError:
        await ctx.send("Format has to be NdN, e.g., 2d6")

# Command: Repeat After Me
@bot.command()
async def say(ctx, *, message: str):
    await ctx.send(message)

# Command: Create Poll
@bot.command()
async def poll(ctx, *, question):
    message = await ctx.send(f"Poll: {question}")
    await message.add_reaction('👍')
    await message.add_reaction('👎')

# Task: Daily Message
@tasks.loop(hours=24)
async def daily_message():
    now = datetime.utcnow()
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="general")
        if channel:
            await channel.send(f"Good morning! The date is {now.strftime('%Y-%m-%d')}.")

@daily_message.before_loop
async def before_daily_message():
    await bot.wait_until_ready()

daily_message.start()

# Command: User Info
@bot.command()
async def userinfo(ctx, member: discord.Member):
    embed = discord.Embed(title=f"{member.name}'s Info", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Status", value=member.status, inline=False)
    embed.add_field(name="Joined", value=member.joined_at, inline=False)
    await ctx.send(embed=embed)

# Command: Server Info
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.green())
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="Created At", value=guild.created_at, inline=False)
    await ctx.send(embed=embed)

# Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing a required argument for this command.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exist.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
    else:
        await ctx.send("An error occurred.")

# Moderation: Kick Member
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked for {reason}.")

# Moderation: Ban Member
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned for {reason}.")

# Moderation: Unban Member
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned.")
            return
    await ctx.send(f"User {member_name} not found in ban list.")

# Voice Channel Join
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel!")

# Voice Channel Leave
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel!")

# Command: Play Music
@bot.command()
async def play(ctx, url: str):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not in a voice channel!")
            return
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        ctx.voice_client.play(discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS))
    await ctx.send(f"Now playing: {info['title']}")

# Command: Stop Music
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Stopped the music.")
    else:
        await ctx.send("I'm not playing any music!")

# Run Bot
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
bot.run(TOKEN)
