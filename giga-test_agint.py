from pathlib import Path
from datetime import datetime, date
from pydantic import BaseModel, Field
from langchain.tools import tool
import uuid
from langgraph.checkpoint.memory import MemorySaver

from langchain_gigachat.chat_models import GigaChat
from langgraph.prebuilt import create_react_agent
from ddgs import DDGS

from GIGACHAT_CREDENTIALS import AuthorizationKey, Scope, ModelGigaChat

# ──────────────────────────────────────────────────────────────
DATA_DIR = Path("agent_data"); DATA_DIR.mkdir(exist_ok=True)

llm = GigaChat(credentials=AuthorizationKey, verify_ssl_certs=False, scope=Scope, model=ModelGigaChat)



# ── append_to_file ──────────────────────────────────────────
class AppendArgs(BaseModel):
    filepath: str = Field(..., description="Имя текстового файла в ./agent_data")
    content:  str = Field(..., description="Текст для записи в файл")

@tool(
    args_schema=AppendArgs,
    description="Добавить строку в локальный текстовый файл (agent_data/...) "
)
def append_to_file(filepath: str, content: str) -> str:
    path  = DATA_DIR / Path(filepath).name                 # без ../
    stamp = datetime.now().strftime("[%d.%m.%Y %H:%M] ")   # DD.MM.YYYY
    with path.open("a", encoding="utf-8") as f:
        f.write(stamp + content.rstrip() + "\n")
    return f"✅ Записано в {path.name}"

# ── search_web ──────────────────────────────────────────────
@tool("search_web", description="Ищет в DuckDuckGo (RU, неделя, 5 ссылок)")
def search_web(query: str, max_results: int = 5) -> str:
    with DDGS() as ddgs:
        hits = ddgs.text(query, region="ru-ru", time="w", max_results=max_results)
        return "\n".join(f"{hit['title']}: {hit['body']} -- {hit['href']}" for hit in hits[:max_results])

# ── агент ───────────────────────────────────────────────────────
today = date.today().strftime("%d.%m.%Y")  # DD.MM.YYYY
system_prompt = (
    f"Сегодня {today}. "
    "Ты полезный ассистент. Используй search_web для поиска в интернете, "
    "append_to_file -- чтобы сохранять результаты."
)


checkpointer = MemorySaver()
agent = create_react_agent(
    model=llm,
    tools=[search_web, append_to_file],
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
    print(f"⚡ Мини-агент с памятью готов (ID диалога: {conversation_id}). Пустая строка -- выход.")

    try:
        while True:
            q = input("> ").strip()
            if not q:
                break
            run(q, conversation_id) # Передаем ID в функцию
    except (KeyboardInterrupt, EOFError):
        pass