import requests

# Intergration API Token
t = ""
# Database query base url
b = "https://api.notion.com/v1/databases/"
# Database id
d = ""
# header
header = {"Authorization": t, "Notion-Version": "2022-06-28"}
# query 조건문
query = {"filter": ""}

# request 라이브러리로 요청.
response = requests.post(b + d + "/query", headers=header, data=query)
print(response.json()["results"])
# [{'object': 'page', 'id': '2dd1e30c-1c3c-4cc3-b00d-157fcc4bd10f', 'created_time': '2023-01-22T16:56:00.000Z', 'last_edited_time': '2023-01-22T16:57:00.000Z', 'created_by': {'object': 'user', 'id': 'e6bf5ee1-fa3f-4e6f-be2a-fa03f302fc19'}, 'last_edited_by': {'object': 'user', 'id': 'e6bf5ee1-fa3f-4e6f-be2a-fa03f302fc19'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': 'fc802683-53ac-4b4e-81eb-47bb2274bc44'}, 'archived': False, 'properties': {'텍스트': {'id': 'ZECN', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': '테스트 용 데이터3', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '테스트 용 데이터3', 'href': None}]}, '태그': {'id': '%7DTmn', 'type': 'multi_select', 'multi_select': [{'id': '5d58a393-d5c5-45bc-bbe9-47ed110b0338', 'name': '태그', 'color': 'blue'}]}, '이름': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': '테스트3', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '테스트3', 'href': None}]}}, 'url': 'https://www.notion.so/3-2dd1e30c1c3c4cc3b00d157fcc4bd10f'}, {'object': 'page', 'id': 'dc932cd6-1e71-4fad-8800-fde6d5bd964e', 'created_time': '2023-01-22T16:56:00.000Z', 'last_edited_time': '2023-01-22T16:57:00.000Z', 'created_by': {'object': 'user', 'id': 'e6bf5ee1-fa3f-4e6f-be2a-fa03f302fc19'}, 'last_edited_by': {'object': 'user', 'id': 'e6bf5ee1-fa3f-4e6f-be2a-fa03f302fc19'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': 'fc802683-53ac-4b4e-81eb-47bb2274bc44'}, 'archived': False, 'properties': {'텍스트': {'id': 'ZECN', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': '테스트 용 데이터2', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '테스트 용 데이터2', 'href': None}]}, '태그': {'id': '%7DTmn', 'type': 'multi_select', 'multi_select': [{'id': '5d58a393-d5c5-45bc-bbe9-47ed110b0338', 'name': '태그', 'color': 'blue'}]}, '이름': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': '테스트2', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '테스트2', 'href': None}]}}, 'url': 'https://www.notion.so/2-dc932cd61e714fad8800fde6d5bd964e'}, {'object': 'page', 'id': 'e587d0fa-ecdb-4101-b523-cc4aa631cac1', 'created_time': '2023-01-22T16:56:00.000Z', 'last_edited_time': '2023-01-22T16:56:00.000Z', 'created_by': {'object': 'user', 'id': 'e6bf5ee1-fa3f-4e6f-be2a-fa03f302fc19'}, 'last_edited_by': {'object': 'user', 'id': 'e6bf5ee1-fa3f-4e6f-be2a-fa03f302fc19'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': 'fc802683-53ac-4b4e-81eb-47bb2274bc44'}, 'archived': False, 'properties': {'텍스트': {'id': 'ZECN', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': '테스트 용 데이터1', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '테스트 용 데이터1', 'href': None}]}, '태그': {'id': '%7DTmn', 'type': 'multi_select', 'multi_select': [{'id': '5d58a393-d5c5-45bc-bbe9-47ed110b0338', 'name': '태그', 'color': 'blue'}]}, '이름': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': '테스트1', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '테스트1', 'href': None}]}}, 'url': 'https://www.notion.so/1-e587d0faecdb4101b523cc4aa631cac1'}]
# 결과 조회 및 파싱
dataLen = len(response.json()["results"])
data = []

for q in response.json()["results"]:
    row = []
    row.append(q["properties"]["이름"]["title"][0]["text"]["content"])
    row.append(q["properties"]["태그"]["multi_select"][0]["name"])
    row.append(q["properties"]["텍스트"]["rich_text"][0]["text"]["content"])
    data.append(row)

print("데이터 가져온 결과 -> ", data)
# 데이터 가져온 결과 ->  [['테스트3', '태그', '테스트 용 데이터3'], ['테스트2', '태그', '테스트 용 데이터2'], ['테스트1', '태그', '테스트 용 데이터1']]