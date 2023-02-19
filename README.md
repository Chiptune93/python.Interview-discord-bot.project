# Discord Bot with Python 

## 개발 환경

- Mac OS 12.5(M1)

- Python 3.10

## 라이브러리 설치

```bash
$ pip install -U discord.py # 디스코드 패키지
$ pip install -U python-dotenv # env 파일로 환경 변수 세팅하기 위해 설치.
$ pip install -U certifi # 인증 관련 문제 발생.
```

## VS Code Extension 설치

- Jupyter
- Jupyter Notebook

## 인증 문제 관련 
- 에러 메세지

```bash
Cannot connect to host discord.com:443 ssl:True [SSLCertVerificationError: (1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)')]
```
     
- 관련 링크 : [#link](https://stackoverflow.com/questions/62108183/discord-py-bot-dont-have-certificate)
- 인증서 관련된 문제로, 파이썬 설치 폴더에서 install Certificates.command 실행으로 해결.
- 폴더 안보여서 그냥 파이썬 홈페이지 가서 새로 설치함.


# 간단한 요청 & 응답 예제

```
Discord-Bot-Tutorial
 ┣ .env
 ┣ bot.py
```

```bash
$ python3 bot.py
```


- 봇이 있는 서버 내 텍스트 채널에서 '$hello' 메세지를 보낼 시, 봇이 'Hello!' 라고 응답하는 예제

```python
@client.event
async def on_message(message):
    print(
        f"{message}"
    )
    
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
```

# Discord with Notion Database - Guide on Youtube

- 디스코드와 노션 데이터베이스 연동을 파이썬으로 작업하는 유튜브 영상.
- link : https://www.youtube.com/watch?v=n8WzcnZYOIM

```
Discord-with-Notion
 ┣ .ipynb_checkpoints
 ┣ notion.ipynb
 ┗ secret.py
```

- Notion 에서 API 통합 하는 방식이 변경되어 아래와 같이 해야 함.

    ![이미지](/md-image/1.png)

- 데이터베이스 가져오기 (항목명)

    ```python
    base_url = "https://api.notion.com/v1/databases/"
    database_id = "44564026-89cf-4d82-9c11-0858a22f2365"

    header = {"Authorization":secretkeys.KEY, "Notion-Version":"2022-06-28"}
    query = {"filter": {"and":[{"property": "category","select": {"equals":"normal-tech"}}]}}

    response = requests.post(base_url + database_id + "/query", headers=header, data=query) 

    def data_parsing(x):
    return [i for i in x]

    data_parsing(response.json()["results"][0]["properties"]) # 0번째 데이터 항목명 가져오는 예제

    # 위에서는 반복 함수 돌렸는데, 그냥 0번째 "질문" 항목 텍스트 가져오기
    response.json()["results"][0]["properties"]["question"]["title"][0]["plain_text"]
    ```

- 서버 내 웹 훅을 통해 채널에 메세지 보내기

    - 디스코드 내 웹 훅 생성

        ![이미지](/md-image/2.png)

    - URL 복사 후, 전송하기

        ```python
        hookData = {
            "content" : out_to_discord,
            "username" : "WebHookBot"
        }

        # Web Hook 으로 메세지 보내기.    
        requests.post(secretkeys.WEB_HOOK_URL, data= hookData)

        ```

## discord.js 가이드

https://v12.discordjs.guide/


## discord.command.ext

```python
from discord.ext import commands
```

- 위와 같은 방식으로 import 하여 사용
- discord.py 보다 직관적인 방식으로 코딩이 가능. 기존 py는 async 한 하나의 함수로 로직을 짜서 안에서 분기 처리하는 방식으로 코딩해야 했기 때문에 함수 사용 및 코딩에 있어서 불편한 감이 있었음.
- 커맨드 방식은 봇에서 처리할 명령 자체를 따로 함수로 구현 후, @command 를 통해 매핑하여 처리할 수 있음.
- 봇 관련된 코딩을 조금 더 정갈하게 할 수 있다는 장점이 있는 것으로 생각됨.
- discord.py 와 같이 사용하면 편함. 예를 들어, 메세지 참조 및 기타 인텐트를 가져와 사용할 때는 discord.py사용, 봇 커맨드 관련 코딩 시에는 commands 사용.

```python
# 사용자가 입력하는 명령어의 프리픽스를 설정한다.
# 여기서 '! '가 되어있으면 사용자는 '! 명령어' 를 입력해야 봇이 반응한다.
prefix = "! "
# 봇 초기화
bot = commands.Bot(command_prefix=prefix, intents=intents)
# 봇에는 기본적으로 헬프 명령어가 잡혀져 있어 따로 'help' 명령어를 구현하고자 한다면
# 봇에서 제거를 해주어야 한다.
bot.remove_command('help')
```

- 위 처럼 봇 명령 시 사용할 prefix를 가지고 시작함.

## Service

1. centOS7 Docker 환경에서 서비스하려면?

    ```bash
    docker run -d -p 8080:80 -e LC_ALL=ko_KR.utf8 -it --name centos centos:7
    docker exec -it centos /bin/bash

    yum install python3

    pip3 install discord.py
    pip3 install python-dotenv
    pip3 install requests

    python3 {pyfile}
    ```

    위 내용을 도커 이미지 OS 상에서 실행 시켜야 했음.

2. 파이썬 라이브러리의 install 방식 

    ```bash
    # 현재 라이브러리 목록을 파일로 떨궈줌
    pip3 freeze > requirements.txt

    # 해당 파일을 읽어서 라이브러리 의존성을 설치
    pip3 install -r requirements.txt
    ```

    해당 방식을 통해 라이브러리 설치를 간소화 할 수 있었음.

3. Dockerfile 구성

기본 CentOS7 이미지 상에서 개발 환경을 세팅하려고 하니 복잡했다.

찾아보니 https://hub.docker.com/_/python 파이썬이 깔려있는 기본 이미지가 있었다.

따라서, 이를 베이스로 다음과 같은 절차를 통해 이미지를 구성하기로 했다

1. 파이썬 베이스 이미지 로딩
2. 라이브러리 설치
3. 파이썬 파일 구동

위 절차를 포함한 dockerfile 을 생성하였다.

```dockerfile
# main image
FROM python:3.10.8-buster 
MAINTAINER chiptune "eoen012@gmail.com"
# 호스트 현재 경로를 /app 경로에 복사
COPY . /app
# 도커 이미지 내 작업 경로를 /app 으로 설정
WORKDIR /app
# 라이브러리 설치 시스템 명령을 실행
RUN pip3 install -r requirements.txt
# 진입점을 python3 로 잡음
ENTRYPOINT ["python3"]
# 명령 인수를 줘서 실행시킴
CMD ["interview-bot-ver2.0.py"]

```

이제 이 파일 기준으로 이미지를 빌드하고 러닝한다.

```bash
docker build . -t bot:{tag}
docker run -d -it --name bot bot:{tag}
```

현재까지 테스트 결과 봇이 잘 동작한다.


# Notion DB CRUD

## 사용자가 데이터 요청할 수 있게 변경하기.

- 사용자가 처음에 데이터를 추가할 수 있도록 하려고 했으나 노션 API의 권한 문제로 인해 해당 기능은 개발 불가했다.
- 대신 사용자가 요청하는 방식으로 제공 DB에 데이터를 넣을 수 있게 변경하려고 한다.
    - 노션 데이터베이스의 각 row는 일반적인 String이나 다른 객체가 아닌 노션의 '페이지' 형태로 저장되기 때문에 API 요청 시에도 데이터베이스 섹션에서 찾을게 아니라 해당 데이터베이스 페이지로 "페이지 생성" 요청을 보내야 한다.
    ([참고 링크](https://stackoverflow.com/questions/69150120/how-to-insert-data-in-database-via-notion-api))

## Notion Dababase 에 데이터 넣기.

- 기본적으로 데이터베이스의 하나의 Row는 사실 Row Data가 아니라, 노션 상 "페이지" 에 해당한다.
- 따라서, 데이터를 넣기 위해서는 페이지 생성 요청을 보내야 생성이 가능하다.

### 어떻게 데이터를 요청할 것인가?

- 페이지 생성 요청을 하기 위해 [공식 페이지](https://developers.notion.com/reference/post-page)에서 살펴보면 생각보다 어떤 형태로 값을 줘야 하는지 불분명 하다.
- 내용을 보고 요청을 작성하고 요청을 실제 보내보면, 어떤 값이 정의되어야 한다는 메세지를 출력해준다.

    ```bash
    {"object":"error","status":400,"code":"validation_error","message":"body failed validation. Fix one:\nbody.properties.question.name should be not present, instead was `\"Project name\"`.\nbody.properties.question.rich_text should be defined, instead was `undefined`.\nbody.properties.question.number should be defined, instead was `undefined`.\nbody.properties.question.url should be defined, instead was `undefined`.\nbody.properties.question.select should be defined, instead was `undefined`.\nbody.properties.question.multi_select should be defined, instead was `undefined`.\nbody.properties.question.people should be defined, instead was `undefined`.\nbody.properties.question.email should be defined, instead was `undefined`.\nbody.properties.question.phone_number should be defined, instead was `undefined`.\nbody.properties.question.date should be defined, instead was `undefined`.\nbody.properties.question.checkbox should be defined, instead was `undefined`.\nbody.properties.question.relation should be defined, instead was `undefined`.\nbody.properties.question.files should be defined, instead was `undefined`.\nbody.properties.question.status should be defined, instead was `undefined`.\nbody.properties.category.id should be defined, instead was `undefined`.\nbody.properties.category.name should be defined, instead was `undefined`.\nbody.properties.category.start should be defined, instead was `undefined`."}
    ```

- 문제는 저기서 추천하는 항목 값들이 필요없는 값이며, 실제 정의하더라도 요청이 200으로 떨어지지 않는다는 점이다.

- 그래서 생각해낸 방법은, 실제 데이터를 쿼리하는 작업을 하면 response에 json형태로 값이 넘어오게 되는데, 이 때 한 데이터만 추출하여 해당 형식을 온라인 json Formatter 로 형식을 맞추어 본 후, 그대로 가져와 사용하는 것이다.

- 예를 들어 다음과 같이 조회된 하나의 데이터가 있다면

    ```bash
    {"object":"page","id":"33f9755e-b839-4240-a221-4afae1039897","created_time":"2023-02-19T08:10:00.000Z","last_edited_time":"2023-02-19T08:10:00.000Z","created_by":{"object":"user","id":"eaaba968-7542-4fbf-bcaf-2768b30a0412"},"last_edited_by":{"object":"user","id":"eaaba968-7542-4fbf-bcaf-2768b30a0412"},"cover":null,"icon":null,"parent":{"type":"database_id","database_id":"44564026-89cf-4d82-9c11-0858a22f2365"},"archived":false,"properties":{"category":{"id":"%3CqCf","type":"select","select":{"id":"6b9385c7-26d1-4720-ad5c-a8bb228959fd","name":"live","color":"green"}},"answer":{"id":"%5DBWd","type":"rich_text","rich_text":[{"type":"text","text":{"content":"높은 응집도와 낮은 결합도를 갖는 코드를 말합니다.","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"높은 응집도와 낮은 결합도를 갖는 코드를 말합니다.","href":null}]},"ref":{"id":"h%3CR_","type":"rich_text","rich_text":[]},"question":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"유연한 코드는 무엇인가요?","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"유연한 코드는 무엇인가요?","href":null}]}},"url":"https://www.notion.so/33f9755eb8394240a2214afae1039897"}
    ```

- 이를 포매터를 이용해 바꿔보면 이렇게 표시된다.

    ```bash
    {
        'object': 'page',
        'id': '2094753a-a4ba-4894-a0b4-4ab2b02d62a0',
        'created_time': '2022-08-22T05:56:00.000Z',
        'last_edited_time': '2023-02-12T14:10:00.000Z',
        'created_by': {
            'object': 'user',
            'id': 'e6bf5ee1-fa3f-4e6f-be2a-fa03f302fc19'
        },
        'last_edited_by': {
            'object': 'user',
            'id': 'e6bf5ee1-fa3f-4e6f-be2a-fa03f302fc19'
        },
        'cover': None,
        'icon': None,
        'parent': {
            'type': 'database_id',
            'database_id': '44564026-89cf-4d82-9c11-0858a22f2365'
        },
        'archived': False,
        'properties': {
            'category': {
                'id': '%3CqCf',
                'type': 'select',
                'select': {
                        'id': '6b9385c7-26d1-4720-ad5c-a8bb228959fd',
                        'name': 'live',
                        'color': 'green'
                }
            },
            'answer': {
                'id': '%5DBWd',
                'type': 'rich_text',
                'rich_text': [
                        {
                            'type': 'text',
                            'text': {
                                'content': '높은 응집도와 낮은 결합도를 갖는 코드를 말합니다.',
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
                            'plain_text': '높은 응집도와 낮은 결합도를 갖는 코드를 말합니다.',
                            'href': None
                        }
                ]
            },
            'ref': {
                'id': 'h%3CR_',
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
                                'content': '유연한 코드는 무엇인가요?',
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
                            'plain_text': '유연한 코드는 무엇인가요?',
                            'href': None
                        }
                ]
            }
        },
        'url': 'https://www.notion.so/2094753aa4ba4894a0b44ab2b02d62a0'
    }
    ```

- 저렇게 표현된 값 중에서, properties 항목만 가지고와 요청에 사용한다. 그러면 요청이 잘못 응답하거나 실패할 일이 없다. 다만 기존에 있는 값 몇개는 빼주어야 한다. 

- 예를 들면, 아이디 값 같은 경우에는 신규로 삽입하는 경우에는 필요없으며, 기타 값들도 주석처리하여 사용 하지 않고 요청을 보낸다.

    ```bash
    'properties': {
            'category': {
                #'id': '%3CqCf',
                'type': 'select',
                'select': {
                    #'id': '6b9385c7-26d1-4720-ad5c-a8bb228959fd',
                    'name': 'request',
                    'color': 'red'
                }
            },
            'answer': {
                #'id': '%5DBWd',
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
                        #'plain_text': '높은 응집도와 낮은 결합도를 갖는 코드를 말합니다.',
                        'href': None
                    }
                ]
            },
            'ref': {
                #'id': 'h%3CR_',
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
                        #'plain_text': '유연한 코드는 무엇인가요?',
                        'href': None
                    }
                ]
            }
        }
    ```

- 사실 문서를 보고 이해하는 것이 향후 사용에 있어 더 편할 수 있겠지만, 뭔가 안맞는 부분이 있는 것 같다.
필요없는 항목인데도 정의되어야 한다고 400에러를 뱉어내는 것을 보면 말이다.

