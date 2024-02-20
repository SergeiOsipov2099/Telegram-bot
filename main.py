import telebot
import requests
import json
from extensions import APIException
from config import TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base}")
        if response.status_code != 200:
            raise APIException("Ошибка при получении курса валюты")
        data = json.loads(response.text)
        if quote not in data["rates"]:
            raise APIException("Неподдерживаемая валюта")
        rate = data["rates"][quote]
        return rate * amount

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для получения курса валют. Для использования отправьте мне сообщение в формате: "
                          "<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой нужно узнать цену первой валюты> <количество первой валюты> Доступные валюты: USD, EUR, RUB")

@bot.message_handler(commands=['values'])
def send_values(message):
    bot.reply_to(message, "Доступные валюты: USD, EUR, RUB")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        text = message.text.split()
        if len(text) != 3:
            raise APIException("Неправильный формат запроса. Пожалуйста, введите данные в формате: <валюта> <валюта> <количество>")
        base_currency, quote_currency, amount = text
        amount = float(amount)
        converted_amount = CurrencyConverter.get_price(base_currency.upper(), quote_currency.upper(), amount)
        bot.reply_to(message, f"{amount} {base_currency.upper()} = {converted_amount:.2f} {quote_currency.upper()}")
    except APIException as e:
        bot.reply_to(message, str(e))
    except ValueError:
        bot.reply_to(message, "Неверный формат количества. Пожалуйста, введите число.")

bot.polling()
