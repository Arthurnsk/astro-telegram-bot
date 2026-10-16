from groq import Groq
from config import GROQ_KEY

client = Groq(api_key=GROQ_KEY)


def generate_forecast(num, num_mean, card, card_mean, rune, rune_mean, moon_phase):
    # Улучшенный промпт для более глубокого стиля
    prompt = f"""
    Ты — древний оракул и мастер эзотерики. Составь мистический прогноз на день.
    Входные данные: 
    - Число дня: {num} ({num_mean})
    - Карта Таро: {card} ({card_mean})
    - Руна: {rune} ({rune_mean})
    - Луна: {moon_phase}

    Стиль: Загадочный, вдохновляющий, лаконичный.
    Формат ответа (строго):
    ЧИСЛО: (1 глубокое предложение)
    ТАРО: (1 глубокое предложение)
    РУНА: (1 глубокое предложение)
    ЛУНА: (1 глубокое предложение)
    ПОСЛАНИЕ: (2 коротких совета от Вселенной)
    """

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7  # Добавляем немного вариативности
        )
        response = completion.choices[0].message.content

        data = {}
        for line in response.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip().upper()] = value.strip()
        return data
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        return None