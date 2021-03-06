import discord
import time
import praw
import random
import json
import asyncio
from datetime import datetime

class RedditWrapper:
    def __init__(self, config):
        self.config = config
        self.reddit = praw.Reddit(client_id=self.config['reddit_client_id'],
                client_secret=self.config['reddit_token'], 
                password=self.config['reddit_password'], 
                user_agent="memator - get memes from a multi", 
                username=self.config['reddit_user'])        
        self.reddit.read_only = True

    def get(self, count=100):
        return [p for p in self.reddit.multireddit(self.config['reddit_user'], self.config['reddit_multi']).new(limit = count)]

class Memator(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        if 'schedule' in self.config and len(self.config['schedule']) > 0:
            print(f"Scheduled calls: {self.config['schedule']}")
            self.bg_task = self.loop.create_task(self.timer())
        self.reddit = RedditWrapper(self.config)

    def auth_and_run(self):
        self.run(self.config['discord_token'])

    async def get_posts_channel(self):
        channel_name = self.config['discord_channel']
        guild = discord.utils.find(lambda g: g.name == self.config['discord_guild'], self.guilds)
    
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)
            existing_channel = discord.utils.get(guild.channels, name=channel_name)
        return existing_channel.id

    async def timer(self):
        await self.wait_until_ready()
        schedule = self.config['schedule']
        cid = await self.get_posts_channel()
        while not self.is_closed():
            weekday = datetime.now().isoweekday() <= 5
            cur_time = time.strftime('%H:%M', time.localtime())
            for s in schedule:
                if s['time'] == cur_time:
                    if 'weekday' in s and s['weekday'] == 1 and weekday == 0:
                        continue
                    print(f'Match: {s}')
                    if 'count' in s:
                        count = s['count']
                    else:
                        count = 1
                    posts = random.choices(self.reddit.get(), k = count)
                    memes = ' '.join([post.url for post in posts])
                    await self.get_channel(cid).send(f"{s['message']}\n{memes}")
            await asyncio.sleep(60)

    async def on_ready(self):
        guild = discord.utils.find(lambda g: g.name == self.config['discord_guild'], self.guilds)
        print(f'{self.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})\n')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

    async def on_message(self, message):
        if message.author == self.user:
            return
    
        if not message.content.startswith('memes'):
            return

        tokens = message.content.split(' ')
        if len(tokens) > 1:
            count = int(tokens[1])
        else:
            count = 1
        posts = random.choices(self.reddit.get(), k = count)
        cid = await self.get_posts_channel()
        if message.channel.id != cid:
            await message.channel.send(f"Your meme is in #{self.config['discord_channel']}! 💯")
        await self.get_channel(cid).send(' '.join([post.url for post in posts]))

client = Memator()
client.auth_and_run()
