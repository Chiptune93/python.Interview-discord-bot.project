# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import random
import time

intents = discord.Intents.all()
prefix = "! "
bot = commands.Bot(command_prefix=prefix,intents=intents)
bot.remove_command('help')

# 사용자 인터뷰 전역 객체
interview = dict()
# 데이터 저장 순서
''' 
interview = {
    'interviewer':'data'
}
data = {
    'score':''              # 점수
    ,'nowIndex':''          # 현재 순서
    ,'interviewData':[]     # 데이터 객체
    ,'time':''              # 문항 당 시간 데이터
    ,'status':''            # 현재 상태 (start/pause)
}
 '''

@bot.event
async def on_ready():
    print("bot is ready!")
    print(bot)
    connectedServer = '[연결된 서버 목록]'
    print(connectedServer)
    print('-------------------------')
    for guild in bot.guilds:
        print(guild)

    print('-------------------------')


@bot.event
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
    if message.type == discord.MessageType.new_member and message.author.name == 'Interview-Bot' and message.author.bot == True:
        await message.channel.send(
            '```'
            + '\n안녕하세요!'
            + '\n해당 봇은 화상 면접을 대비하여, 질문에 대한 응답을 연습할 수 있도록 제공되는 봇입니다.'
            + '\n감사합니다 :D'
            + '\n'
            + '\n[지원되는 명령]'
            + '\n! help > 도움말'
            + '\n! start > 시작'
            + '\n! stop > 종료 및 점수 출력'
            + '\n! pause > 일시 정지 (고려)'
            + '\n! set time [number] > 문항 당 시간'
            + '```'
        )
    elif message.author.bot == True:
        return
    else:
        await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    print("on guild join event")
    print(guild)


@bot.command()
async def help(message):
    print("send help message")
    await message.channel.send(
        '```'
        + '\n안녕하세요!'
        + '\n해당 봇은 화상 면접을 대비하여, 질문에 대한 응답을 연습할 수 있도록 제공되는 봇입니다.'
        + '\n감사합니다 :D'
        + '\n'
        + '\n[지원되는 명령]'
        + '\n! help > 도움말'
        + '\n! start > 시작'
        + '\n! stop > 종료 및 점수 출력'
        + '\n! pause > 일시 정지 (고려)'
        + '\n! set time [number] > 문항 당 시간'
        + '```'
    )

@bot.command()
async def start(message):
    print(message)
    # 명령자 아이디
    member_id = message.author.id
    print("member id : " , member_id)
    
    if interview.get(member_id) != None:
        interview_data = interview.get(member_id)
    else:
        # 데이터 객체 초기화
        interview_data = {
            'data': notion_data_set()   # 인터뷰 데이터
            ,'score':0                  # 점수
            ,'nowIndex':0               # 현재 순서
            ,'time':30                  # 문항 당 시간 데이터
            ,'status':'stop'            # 현재 상태 (start/pause/stop)
        }
        interview[member_id] = interview_data
    
    # 인터뷰 시작
    await message.channel.send(
        '```'
        + '\n안녕하세요!'
        + '\n곧 인터뷰를 시작하겠습니다.'
        + '```'
    )
    time.sleep(5)
    
    index = 0
    # ToDo 1. 질문 데이터에 공백 있으면 짤림
    # Todo 2. 슬립 때문에 비동기 이벤트 처리 지연되면 디스코드 게이트웨이에서 연결 끊음
    # Todo -> 전체 자동은 못하고, 질문 하나 던지고 사용자 입력 받아 정답 출력 후, 다음으로 이동 하는 등 사용자 입력을 통해 질문 넘기는 방식으로 변경해야 함.
    for question in interview_data.get('data'):
        print(question)
        interview_data['nowIndex'] = index
        print("Q : ", question[0])
        print("A : ", question[1])
        await message.channel.send(
            '```'
            + '\n문제 ' + str(index+1) + '.\n'
            + question[0]
            + '```'
        )
        time.sleep(interview_data.get('time'))
        await message.channel.send(
            '```'
            + '\n정답 ' + str(index+1) + '.\n'
            + question[1]
            + '```'
        )
        index += 1
    
    

def notion_data_set():
    t = os.getenv('NOTION_API_TOKEN')
    b = "https://api.notion.com/v1/databases/"
    d = "44564026-89cf-4d82-9c11-0858a22f2365"
    header = {"Authorization": t, "Notion-Version": "2022-06-28"}
    query = {"filter": {
        "and": [{"property": "category", "select": {"equals": "normal-tech"}}]}}

    response = requests.post(b + d + "/query", headers=header, data=query)
    print("result data length -> ", len(response.json()["results"]))
    dataLen = len(response.json()["results"])
    data = []

    for q in response.json()["results"]:
        row = []
        row.append(q["properties"]["question"]["title"][0]["plain_text"])
        row.append(q["properties"]["answer"]["rich_text"][0]["plain_text"])
        data.append(row)
    
    # 가져온 데이터 랜덤화
    data = list(data)
    random.shuffle(data)
    return data


load_dotenv()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
