# bot.py
import os

import discord
from dotenv import load_dotenv

import requests
import asyncio

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
    
    # 온 메세지 함 수 내에서 정의해버리면 모든 메세지가 올 때마다 (서버 상관 없이)
    # 데이터를 가져오고 초기화 함 ... 초기화 하고, 상태 (시작/중지/종료) 에 따라 데이터가
    # 바뀌는 등의 작업을 어떻게 해야할 지 고민이 필요함.
    # notion database data
    data = notion_data_set()

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
        
    elif message.author.bot == False and message.content.startswith('! help'):
        # help message
        await send_help_message(message)
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
    else:
        return


async def send_help_message(message):
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


def chk_interview_now():
    print("chk interview now")


def interview_start():
    print("interview start")


def interview_stop():
    print("interview stop")


def interview_pause():
    print("interview pause")


def interview_set_time():
    print("interview set time")


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

    print(data)
    return data


client.run(TOKEN)
