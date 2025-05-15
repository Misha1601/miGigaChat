"""Пример работы с чатом через gigachain"""
from GIGACHAT_CREDENTIALS import ClientID, Scope
from langchain.schema import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

# giga = GigaChat(
    # Для авторизации запросов используйте ключ, полученный в проекте GigaChat API
#     credentials=Scope,
#     verify_ssl_certs=False,
# )

# messages = [
#     SystemMessage(
#         content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
#     )
# ]

# while(True):
#     user_input = input("Пользователь: ")
#     if user_input == "пока":
#       break
#     messages.append(HumanMessage(content=user_input))
#     res = giga.invoke(messages)
#     messages.append(res)
#     print("GigaChat: ", res.content)

import requests

def get_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload='scope=GIGACHAT_API_PERS'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': '<ВАШ Client Secret>',
    'Authorization': 'Basic <ВАШИ Данные Авторизации>'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')

    return response.json()

print(get_token())

