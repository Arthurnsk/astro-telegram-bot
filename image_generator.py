import requests
import random
import io
import urllib.parse


def get_image(card_name):
    # Космические теги для поиска
    space_themes = ["cosmos", "galaxy", "nebula", "stars", "deep-space"]
    theme = random.choice(space_themes)

    # 1. Сначала пробуем ИИ (Pollinations)
    seed = random.randint(1, 99999)
    query = f"mystical tarot card {card_name}, cinematic space, high resolution"
    encoded_query = urllib.parse.quote(query)
    ai_url = f"https://image.pollinations.ai/prompt/{encoded_query}?seed={seed}&width=800&height=800&nologo=true"

    try:
        response = requests.get(ai_url, timeout=15)
        if response.status_code == 200 and len(response.content) > 1000:  # Проверка, что это не пустой файл
            img_byte_arr = io.BytesIO(response.content)
            img_byte_arr.seek(0)  # Важно: сбрасываем указатель в начало
            return img_byte_arr
    except:
        print("ИИ не ответил, переходим к запасному фото...")

    # 2. ЗАПАСНОЙ ВАРИАНТ: LoremFlickr (намного надежнее Unsplash сейчас)
    fallback_url = f"https://loremflickr.com/800/800/{theme}"
    try:
        response = requests.get(fallback_url, timeout=15)
        if response.status_code == 200:
            img_byte_arr = io.BytesIO(response.content)
            img_byte_arr.seek(0)
            return img_byte_arr
    except Exception as e:
        print(f"Даже запасной сервис не ответил: {e}")

    return None