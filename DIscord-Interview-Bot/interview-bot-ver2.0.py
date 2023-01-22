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
bot = commands.Bot(command_prefix=prefix, intents=intents)
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
            + '\n! next > 다음 문제 보기'
            + '\n! ans > 현재 문제 정답 보기'
            + '\n! fin > 종료 및 점수 출력'
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
        + '\n! next > 다음 문제 보기'
        + '\n! ans > 현재 문제 정답 보기'
        + '\n! fin > 종료 및 점수 출력'
        + '```'
    )


@bot.command()
async def start(message):
    print(message)
    # 명령자 아이디
    member_id = message.author.id
    print("member id : ", member_id)

    if interview.get(member_id) != None:
        interview_data = interview.get(member_id)
    else:
        # 데이터 객체 초기화
        interview_data = {
            'data': notion_data_set()   # 인터뷰 데이터
            , 'score': 0                  # 점수
            , 'nowIndex': 0               # 현재 순서
            , 'status': 'stop'            # 현재 상태 (start/pause/stop)
        }
        interview[member_id] = interview_data

    # 인터뷰 시작
    await message.channel.send(
        '```'
        + '\n안녕하세요!'
        + '\n곧 인터뷰를 시작하겠습니다.'
        + '```'
    )
    time.sleep(3)
    # 현재 인덱스 지정 후, 다음 실행.
    interview_data['nowIndex'] = -1
    await next(message)

    # ToDo 1. 질문 데이터에 공백 있으면 짤림
    # Todo 2. 슬립 때문에 비동기 이벤트 처리 지연되면 디스코드 게이트웨이에서 연결 끊음
    # Todo -> 전체 자동은 못하고, 질문 하나 던지고 사용자 입력 받아 정답 출력 후, 다음으로 이동 하는 등 사용자 입력을 통해 질문 넘기는 방식으로 변경해야 함.


@bot.command()
async def next(message):
    # 명령자 아이디
    member_id = message.author.id

    interview_data = interview.get(member_id)
    if interview_data == None:
        await message.channel.send(
            '```'
            + '\n인터뷰가 진행 중이지 않습니다. ! start 를 통해, 인터뷰를 시작해주세요.'
            + '```'
        )
    else:
        nowIndex = interview_data['nowIndex'] + 1
        interview_data['nowIndex'] = nowIndex
        dataSet = interview_data.get('data')[nowIndex]
        q = dataSet[0]
        a = dataSet[1]
        print("now index is : ", nowIndex)
        print("index question : ", q)
        print("index answer : ", a)

        await message.channel.send(
            '```'
            + '\n[문제]\n'
            + q
            + '```'
        )


@bot.command()
async def ans(message):
    # 명령자 아이디
    member_id = message.author.id

    interview_data = interview.get(member_id)
    if interview_data == None:
        await message.channel.send(
            '```'
            + '\n인터뷰가 진행 중이지 않습니다. ! start 를 통해, 인터뷰를 시작해주세요.'
            + '```'
        )
    else:
        nowIndex = interview_data['nowIndex']
        dataSet = interview_data.get('data')[nowIndex]
        q = dataSet[0]
        a = dataSet[1]
        print("now index is : ", nowIndex)
        print("index question : ", q)
        print("index answer : ", a)

        await message.channel.send(
            '```'
            + '\n[답변]\n'
            + a
            + '```'
        )


@bot.command()
async def fin(message):
    # 명령자 아이디
    member_id = message.author.id

    interview_data = interview.get(member_id)
    if interview_data == None:
        await message.channel.send(
            '```'
            + '\n인터뷰가 진행 중이지 않습니다. ! start 를 통해, 인터뷰를 시작해주세요.'
            + '```'
        )
    else:
        nowIndex = interview_data['nowIndex']
        await message.channel.send(
            '```'
            + '\n인터뷰 종료! '
            + '\n총 문제 수 : ' + str(len(interview_data.get('data')))
            + '\n총 답변 수 : ' + str(nowIndex + 1)
            + '\n수고 하셨습니다 :D'
            + '```'
        )
        del interview[member_id]


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

    print(response.json()["results"])

    for q in response.json()["results"]:
        row = []
        row.append(q["properties"]["question"]["title"][0]["text"]["content"])
        row.append(q["properties"]["answer"]
                   ["rich_text"][0]["text"]["content"])
        data.append(row)

    # 가져온 데이터 랜덤화
    data = list(data)
    random.shuffle(data)
    return data


load_dotenv()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
