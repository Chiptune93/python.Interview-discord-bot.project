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

centOS7 Docker 환경에서 서비스

```bash
docker run -d -p 8080:80 -e LC_ALL=ko_KR.utf8 -it --name centos centos:7
docker exec -it centos /bin/bash

yum install python3

pip3 install discord.py
pip3 install python-dotenv
pip3 install requests

python3 {pyfile}
```