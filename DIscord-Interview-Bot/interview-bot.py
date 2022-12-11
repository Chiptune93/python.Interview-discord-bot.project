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

    
@client.event
async def on_message(message):
    print("---------------------------")
    print("message all -> ", message)
    print("---------------------------")
    print("guild name           -> ", message.guild.name)
    print("channel name         -> ", message.channel.name)
    print("message type         -> ", message.type)
    print("message sender       -> ", message.author.name)
    print("message bot y/n      -> ", message.author.bot)
    print("message content      -> ", message.content)
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
        
    elif message.author.bot == False and message.content.startswith('! help'):
        # help message
        send_help_message()
    elif message.author.bot == False and message.content.startswith('! start'):
        # start
        # 현재 인터뷰 중인지 체크
        if chk_interview_now():
            # 인터뷰 중이면 명령 실행 X
            return
        else:
            # 인터뷰 시작.
            interview_start()
    elif message.author.bot == False and message.content.startswith('! stop'):
        # stop
        # 현재 인터뷰 중인지 체크
        if chk_interview_now():
            # 인터뷰 중이면 중지.
            interview_stop()
        else:
            # 인터뷰 중이 아니면 명령 실행 X
            return
    elif message.author.bot == False and message.content.startswith('! pause'):
        # pause
        # 현재 인터뷰 중인지 체크
        if chk_interview_now():
            # 인터뷰 중이면 일시 정지
            interview_pause()
        else:
            # 인터뷰 중이 아니면 명령 실행 X
            return
    elif message.author.bot == False and message.content.startswith('! set time'):
        # set time
        # 현재 인터뷰 중인지 체크
        if chk_interview_now():
            # 인터뷰 중이면 명령 실행
            interview_set_time()
        else:
            # 인터뷰 중이 아니면 명령 실행 X
            return
        
    # other message ignore! 
    else :
        return


client.run(TOKEN)


async def send_help_message():
    print("send help message")
    
    
async def chk_interview_now():
    print("chk interview now")
    
    
async def interview_start():
    print("interview start")
    
    
async def interview_stop():
    print("interview stop")
    
    
async def interview_pause():
    print("interview pause")
    
    
async def interview_set_time():
    print("interview set time")