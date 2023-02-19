# -*- coding: utf-8 -*-
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import random
import time

# 기본제공 데이터베이스 아이디
default_db_id = "44564026-89cf-4d82-9c11-0858a22f2365"

intents = discord.Intents.all()
# 사용자가 입력하는 명령어의 프리픽스를 설정한다.
# 여기서 '! '가 되어있으면 사용자는 '! 명령어' 를 입력해야 봇이 반응한다.
prefix = "! "
# 봇 초기화
bot = commands.Bot(command_prefix=prefix, intents=intents)
# 봇에는 기본적으로 헬프 명령어가 잡혀져 있어 따로 'help' 명령어를 구현하고자 한다면
# 봇에서 제거를 해주어야 한다.
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


@bot.event
async def on_message(message):
    # 새로운 서버에 봇이 추가되었을 때, welcome message
    if message.type == discord.MessageType.new_member and message.author.name == 'Interview-Bot' and message.author.bot == True:
        await message.channel.send(
            '```'
            + '\n안녕하세요!'
            + '\n해당 봇은 화상 면접을 대비하여, 질문에 대한 응답을 연습할 수 있도록 제공되는 봇입니다.'
            + '\n질문 등록 요청 시, 띄어쓰기로 질문과 답변을 구분하기 때문에 띄어쓰기 없이 요청 하셔야 제대로 확인 후 등록이 가능합니다.'
            + '\n감사합니다 :D'
            + '\n'
            + '\n[지원되는 명령]'
            + '\n! help > 도움말'
            + '\n! start > 시작'
            + '\n! next > 다음 문제 보기'
            + '\n! ans > 현재 문제 정답 보기'
            + '\n! fin > 종료 및 점수 출력'
            + '\n! req_data 질문 답변 > 질문 등록 요청하기.'
            + '```'
        )
    elif message.author.bot == True:
        return
    else:
        # 데이터 요청 전처리
        if message.content.startswith("! req_data"):
            # 데이터 요청인 경우, 별도의 프로세스 적용
            question = ""
            answer = ""
            try:
                question = message.content.split(
                    '! req_data')[1].split('[,]')[0]
                answer = message.content.split('! req_data')[1].split('[,]')[1]
            except:
                await message.channel.send(
                    '```'
                    + '\n질문 등록 요청이 양식에 맞지 않습니다.'
                    + '```'
                )
                return

            if len(question) < 1 or len(answer) < 1:
                await message.channel.send(
                    '```'
                    + '\n질문 등록 요청이 양식에 맞지 않습니다.'
                    + '```'
                )
                return
            else:
                res = notion_data_create('', question, answer)
                if res == 200:
                    await message.channel.send(
                        '```'
                        + '\n질문 등록 요청에 성공 하였습니다.'
                        + '```'
                    )
                else:
                    await message.channel.send(
                        '```'
                        + '\n질문 등록 요청에 실패 하였습니다.'
                        + '```'
                    )
        else:
            # 아닌 경우 프로세스 진행
            await bot.process_commands(message)


@bot.event
async def on_guild_join(guild):
    print("on guild join event")


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
    # 명령자 아이디
    member_id = message.author.id
    print("member id : ", member_id)

    if interview.get(member_id) != None:
        interview_data = interview.get(member_id)
    else:
        # 데이터 객체 초기화
        interview_data = {
            'data': notion_data_set("")   # 인터뷰 데이터
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


#@bot.command()
#async def req_data(message, arg1, arg2):
#    # 명령자 아이디
#    member_id = message.author.id
#    print("member id : ", member_id)
#    print("arg1 : ", arg1)  # 질문
#    print("arg2 : ", arg2)  # 답변
#    print(message)
#    print(message.args)
#    print(message.kwargs)
#    print(message.message)
#    print(message.current_argument)


def notion_data_set(dbid):
    if dbid == None or dbid == '':
        dbid = default_db_id
    t = os.getenv('NOTION_API_TOKEN')
    b = "https://api.notion.com/v1/databases/"
    d = dbid
    header = {"Authorization": t, "Notion-Version": "2022-06-28"}
    query = {"filter": {
        "and": [{"property": "category", "select": {"equals": "live"}}]}}

    response = requests.post(b + d + "/query", headers=header, data=query)
    data = []

    print(response.json()["results"][0])

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


def notion_data_create(dbid, arg1, arg2):
    if dbid == None or dbid == '':
        dbid = default_db_id
    t = os.getenv('NOTION_API_TOKEN')
    b = "https://api.notion.com/v1/pages/"
    d = dbid
    header = {
        "Authorization": t,
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }
    payload = {
        "parent": {
            "database_id": dbid
        },
        'properties': {
            'category': {
                # 'id': '%3CqCf',
                'type': 'select',
                'select': {
                    # 'id': '6b9385c7-26d1-4720-ad5c-a8bb228959fd',
                    'name': 'request',
                    'color': 'red'
                }
            },
            'answer': {
                # 'id': '%5DBWd',
                'type': 'rich_text',
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                            'content': arg2,
                            'link': None
                        },
                        'annotations': {
                            'bold': False,
                            'italic': False,
                            'strikethrough': False,
                            'underline': False,
                            'code': False,
                            'color': 'default'
                        },
                        # 'plain_text': '높은 응집도와 낮은 결합도를 갖는 코드를 말합니다.',
                        'href': None
                    }
                ]
            },
            'ref': {
                # 'id': 'h%3CR_',
                'type': 'rich_text',
                'rich_text': [
                ]
            },
            'question': {
                'id': 'title',
                'type': 'title',
                'title': [
                    {
                        'type': 'text',
                        'text': {
                            'content': arg1,
                            'link': None
                        },
                        'annotations': {
                            'bold': False,
                            'italic': False,
                            'strikethrough': False,
                            'underline': False,
                            'code': False,
                            'color': 'default'
                        },
                        # 'plain_text': '유연한 코드는 무엇인가요?',
                        'href': None
                    }
                ]
            }
        }
    }

    response = requests.post(b, headers=header, json=payload)
    return response.text


load_dotenv()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
