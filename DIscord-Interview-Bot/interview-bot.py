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
async def on_guild_join(guild):
   print("on guild join event")
   print(guild)
   
    

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
    print("---------------------------")
    print("message > ", message)
    print("message > ", message.type)
    print("message > ", message.author)
    print("message > ", message.author.bot)
    print("---------------------------")
    
    # 새로운 서버에 봇이 추가되었을 때, welcome message
    if message.type == discord.MessageType.new_member and message.author.name == 'Interview-Bot' and message.author.bot == True :
        await message.channel.send(
            '```'
            +'\n안녕하세요!'
            +'\n해당 봇은 화상 면접을 대비하여, 질문에 대한 응답을 연습할 수 있도록 제공되는 봇입니다.'
            +'\n감사합니다 :D'
            +'\n'
            +'\n[지원되는 명령]'
            +'\n! help > 도움말'
            +'\n! start > 시작'
            +'\n! stop > 종료 및 점수 출력'
            +'\n! pause > 일시 정지 (고려)'
            +'\n! set time [number] > 문항 당 시간'
            + '```'
        )

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(TOKEN)
