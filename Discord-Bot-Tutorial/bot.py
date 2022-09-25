# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

TEST_GUILD_NAME = os.getenv('TEST_GUILD_NAME')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    # 연결 시 디버깅 코멘트 출력
    # print('Connected!')
    # 단순 객체를 반복하여 출력
    # for guild in client.guilds:
    # if guild.name == TEST_GUILD_NAME:
    #     break
    
    # 람다를 활용한 방식
    # guild = discord.utils.find(
    #     lambda g: g.name == TEST_GUILD_NAME, client.guilds)

    # discord util의 get을 활용.
    guild = discord.utils.get(client.guilds, name=TEST_GUILD_NAME)
    
    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    
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
