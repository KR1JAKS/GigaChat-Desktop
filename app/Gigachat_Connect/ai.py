from gigachat import GigaChat
import winsound
import threading
from app.Config import config

giga = GigaChat(credentials="Authorization Key", #Замените Authorization Key на свой
                verify_ssl_certs=False)

def success():
    winsound.PlaySound('app\\Resources\\Sounds\\message.wav', winsound.SND_FILENAME)

def error():
    winsound.PlaySound('app\\Resources\\Sounds\\error.wav', winsound.SND_FILENAME)

def chat_ai(question):
    payload = {
        'messages' : [
            {'role': 'user', 'content' : question}
    ]
}

    try:
        response = giga.chat(payload)
        if hasattr(response, 'choices') and len(response.choices) > 0:
            threading.Thread(target=success).start()
            return response.choices[0].message.content
    except Exception:
           threading.Thread(target=error).start()
           return f'Ошибка: нет доступа в интернет!'
