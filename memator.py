import discord
import praw
import random
import json

with open('config.json', 'r') as f:
    config = json.load(f)

client = discord.Client()

reddit = praw.Reddit(client_id=config['reddit_client_id'],
        client_secret=config['reddit_token'], 
        password=config['reddit_password'], 
        user_agent="memator - get memes from a multi", 
        username=config['reddit_user'])        
reddit.read_only = True

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == config['discord_guild'], client.guilds)
    print(f'{client.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})\n')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    
@client.event
async def on_message(message):
    channel_name = config['discord_channel']
    guild = discord.utils.find(lambda g: g.name == config['discord_guild'], client.guilds)

    if message.author == client.user:
        return

    if message.content == channel_name:
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)
            existing_channel = discord.utils.get(guild.channels, name=channel_name)

        posts = reddit.multireddit(config['reddit_user'], config['reddit_multi']).new(limit = 100)
        p = random.choice([p for p in posts])
        await message.channel.send(f"Your meme is in #{channel_name}! 💯")
        await client.get_channel(existing_channel.id).send(p.url)

client.run(config['discord_token'])
