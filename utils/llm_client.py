import os
# pyrefly: ignore [missing-import]
from openai import OpenAI

from agents.agent import SYSTEM_PROMPT

MODEL = "openai/gpt-oss-120b"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)


def send(user_message, history=None):
    """Отправляет сообщение агенту через OpenRouter, возвращает текст ответа и обновлённую историю."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + (history or []) + [
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create( # отправляем запрос модели
        model=MODEL,
        messages=messages,
    )

    text = response.choices[0].message.content # берем текст ответа агента
    updated_history = (history or []) + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": text},
    ]

    return {"text": text, "history": updated_history} 
