# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
print(TOKEN)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("bot is ready!")
    guild = discord.utils.get(client.guilds)
    
    connectedServer = '[연결된 서버 목록]'
    print(connectedServer)
    print('-------------------------')
    for guild in client.guilds:
        print(guild)
    
    print('-------------------------')
    


# 간단한 요청 & 응답 예제
# 서버 내 채널에서 '$hello' 보낼 시, 봇이 'Hello!' 응답.
@client.event
async def on_message(message):
    print(
        f"{message}"
    )

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(TOKEN)
