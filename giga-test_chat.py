from datetime import date
import uuid
from langgraph.checkpoint.memory import MemorySaver

from langchain_gigachat.chat_models import GigaChat
from langgraph.prebuilt import create_react_agent

from GIGACHAT_CREDENTIALS import AuthorizationKey, Scope, ModelGigaChat

# ──────────────────────────────────────────────────────────────
llm = GigaChat(credentials=AuthorizationKey, verify_ssl_certs=False, scope=Scope, model=ModelGigaChat)


# ── агент ───────────────────────────────────────────────────────
today = date.today().strftime("%d.%m.%Y")  # DD.MM.YYYY
system_prompt = ("Ты полезный ассистент по психологии.")

checkpointer = MemorySaver()
agent = create_react_agent(
    model=llm,
    prompt=system_prompt,
    checkpointer=checkpointer # Подключаем "память" к агенту
)
# ── REPL ───────────────────────────────────────────────────
def run(query: str, thread_id: str): # Принимаем ID диалога
    config = {"configurable": {"thread_id": thread_id}}
    resp = agent.invoke({"messages": [("user", query)]}, config=config)
    for message in resp["messages"]:
        message.pretty_print()

if __name__ == "__main__":
    # Создаем уникальный ID для всей сессии нашего диалога
    conversation_id = str(uuid.uuid4())
    print(f"---------{today}---------")
    print(f"⚡ Мини-агент с памятью готов (ID диалога: {conversation_id}). Пустая строка -- выход.")

    try:
        while True:
            q = input("> ").strip()
            if not q:
                break
            run(q, conversation_id) # Передаем ID в функцию
    except (KeyboardInterrupt, EOFError):
        pass