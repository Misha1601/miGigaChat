import requests
import json
import uuid


from GIGACHAT_CREDENTIALS import ClientID, ClientSecret, Scope, AuthorizationKey
client_id = ClientID
secret = ClientSecret
auth = AuthorizationKey

def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
      Выполняет POST-запрос, который выдает токен.
      Параметры:
      - auth_token (str): токен авторизации, необходимый для запроса.
      - область (str): область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».
      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    # Создадим идентификатор UUID
    rq_uid = str(uuid.uuid4())
    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }
    # Тело запроса
    payload = {
        'scope': scope
    }
    try:
        # Делаем POST запрос с отключенной SSL верификацией
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1

def get_chat_completion(auth_token, user_message):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat.
    Параметры:
    - auth_token (str): Токен для авторизации в API.
    - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.
    Возвращает:
    - str: Ответ от API в виде текстовой строки.
    """
    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat",  # Используемая модель
        "messages": [
            {
                'role': 'system',
                'content': 'Ты профессиональный редактор текстов. Приведи текст к более официальному стилю. Верни только откорректированный текст. Если корректировка не требуется, то верни только сообщение «Текст соответствует официальному стилю».',
            },
            {
                "role": "user",  # Роль отправителя (пользователь)
                "content": user_message  # Содержание сообщения
            }
        ],
        "temperature": 1,  # Температура генерации
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": 512,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения
        "update_interval": 0  # Интервал обновления (для потоковой передачи)
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    # Выполнение POST-запроса и возвращение ответа
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return -1

def get_delays_token(auth_token):
    """Возвращает доступный остаток токенов для каждой из моделей. Метод доступен только при покупке пакетов токенов."""
    url = "https://gigachat.devices.sberbank.ru/api/v1/balance"
    payload = {}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Bearer {auth_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    print(response.text)

def get_mdels(auth_token):
    """Получить список моделей"""
    url = "https://gigachat.devices.sberbank.ru/api/v1/models"
    payload = {}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Bearer {auth_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    print(response.text)

# Получаем токен доступа
response = get_token(auth)
giga_token = response.json()['access_token']
print(giga_token)
# Сделаем запрос к GigaChat
# text = """В соответствии с приказом от 19 февраля 2024 года № 1-02/26 «Об утверждении Положения о порядке оформления, учета и выдачи доверенности в ФГБУ ИАЦ Судебного департамента», направляю Вам оригинал доверенности от 15 января 2025 года № 3, выданной Никифорову Михаилу Михайловичу, на период с 10 до 21 февраля 2025 года включительно. Срок действия доверенности истёк."""
# answer = get_chat_completion(giga_token, text)
# print(answer.json()['choices'][0]['message']['content'])
# проверим остаток доступных токенова
get_delays_token(giga_token)
# получаем список доступных моделей
get_mdels(giga_token)
