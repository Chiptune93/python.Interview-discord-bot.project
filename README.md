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