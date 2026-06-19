import requests
import json
from datetime import datetime

user_name = None
messages_count = 0
mood = "🙂 нейтральное"
character = "дружелюбный"
dialog_history = []
forbidden_words = ['болт','палатка']


def send(question):
    global mood, character

    for word in forbidden_words:
        if word in question.lower():
            mood = 'сердитое'
            character = 'злой водитель овощевоза из Венгрии'
            print('Произошла смена характера')
            break

    prompt = f"""
            Ты виртуальный друг пользователя.
            Твое настроение {mood},
            твой характер {character}.
            Пользователь говорит тебе {question}.
            Отвечай на русском языке.
            """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer api key",
                "Content-Type": "application/json",
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>",
            },
            data=json.dumps({
                "model": "openrouter/owl-alpha",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            })
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException:
        return "❌ Ошибка соединения с сервером."
    except KeyError:
        return "❌ Некорректный ответ от API."
    except Exception as e:
        return f"❌ Ошибка: {e}"


while True:
    message = input('Ваши слова: ')
    response = send(message)
    print(response)