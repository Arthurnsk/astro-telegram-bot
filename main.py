import logging
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from config import BOT_TOKEN, CHANNEL_ID, POST_TIME
import time

# Импорты ваших модулей
from tarot import get_tarot
from runes import get_rune
from numerology import get_number
from astrology import moon
from ai import generate_forecast
from image_generator import get_image

# 1. Настройка логирования (чтобы видеть ошибки в файле)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot_log.log'
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")


def generate_full_data():
    """Сборка всех данных и генерация контента"""
    logger.info("Начало генерации прогноза...")
    try:
        card, card_mean = get_tarot()
        rune, rune_mean = get_rune()
        num, num_mean = get_number()
        moon_phase = moon()

        ai_data = generate_forecast(num, num_mean, card, card_mean, rune, rune_mean, moon_phase)

        if ai_data:
            txt_num = ai_data.get("ЧИСЛО", f"Вибрации {num_mean}")
            txt_tarot = ai_data.get("ТАРО", f"Влияние {card_mean}")
            txt_rune = ai_data.get("РУНА", f"Сила {rune_mean}")
            txt_moon = ai_data.get("ЛУНА", f"Фаза {moon_phase}")
            txt_msg = ai_data.get("ПОСЛАНИЕ", "Доверяйте знакам Вселенной.")
        else:
            txt_num, txt_tarot, txt_rune, txt_moon, txt_msg = "...", "...", "...", "...", "..."

        photo = get_image(card)

        text = (
            f"🌟 *ДНК ДНЯ*\n\n"
            f"🔢 *ЧИСЛО ДНЯ:* {num}\n{txt_num}\n\n"
            f"🎴 *КАРТА ТАРО:* {card}\n{txt_tarot}\n\n"
            f"ᛉ *РУНА ДНЯ:* {rune}\n{txt_rune}\n\n"
            f"🌙 *ЛУННАЯ ФАЗА*\n{txt_moon}\n\n"
            f"✨ *ПОСЛАНИЕ ВСЕЛЕННОЙ*\n{txt_msg}\n\n"
            f"#астрология #прогноз #энергиядня"
        )
        return text, photo
    except Exception as e:
        logger.error(f"Критическая ошибка при генерации: {e}")
        return "Ошибка генерации прогноза.", None


def send_daily_post():
    """Функция для планировщика"""
    logger.info("Запуск автоматического постинга в канал...")
    text, photo = generate_full_data()
    try:
        if photo:
            if len(text) <= 1024:
                bot.send_photo(CHANNEL_ID, photo=photo, caption=text)
            else:
                bot.send_photo(CHANNEL_ID, photo=photo)
                bot.send_message(CHANNEL_ID, text)
        else:
            bot.send_message(CHANNEL_ID, text)
        logger.info("Пост успешно отправлен.")
    except Exception as e:
        logger.error(f"Ошибка отправки поста: {e}")


# --- Обработчики команд ---

@bot.message_handler(commands=["start"])
def start(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔮 Получить прогноз")
    bot.send_message(msg.chat.id, "Добро пожаловать в систему ДНК ДНЯ!", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "🔮 Получить прогноз")
def manual_predict(msg):
    bot.send_chat_action(msg.chat.id, 'upload_photo')
    text, photo = generate_full_data()
    if photo:
        bot.send_photo(msg.chat.id, photo=photo, caption=text)
    else:
        bot.send_message(msg.chat.id, text)


# --- Инициализация и запуск ---

if __name__ == "__main__":
    # Настраиваем планировщик
    scheduler = BackgroundScheduler(timezone="Europe/Moscow")
    # Добавляем задачу: каждый день в POST_TIME
    hour, minute = POST_TIME.split(":")
    scheduler.add_job(send_daily_post, 'cron', hour=hour, minute=minute)
    scheduler.start()

    logger.info("Бот запущен. Планировщик активен.")

    # Запуск бота в бесконечном цикле
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.critical(f"Бот упал: {e}")