"""Пример работы с чатом через gigachain"""
from GIGACHAT_CREDENTIALS import Scope
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=Scope)

messages = [
    SystemMessage(
        content="Ты специалист по английскому языку, который помогает его изучать"
    )
]
# print(chat.get_models())
# print(chat.tokens_count(['Привет, ты кто?', 'Я властелин мира жажущий покоя!']))
# print(chat.get_num_tokens('Я властелин мира жажущий покоя!'))
while(True):
    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    print("Bot: ", res.content)

