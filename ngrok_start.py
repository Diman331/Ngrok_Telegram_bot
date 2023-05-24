import telebot
import subprocess
import requests
import time
import json
import psutil
from telebot import types
from functools import wraps


bot = telebot.TeleBot('ТОКЕН_ВАШЕГО_БОТА')

commands = [
    telebot.types.BotCommand("ngrok", "Запуск"),
    telebot.types.BotCommand("ngrok_stop", "Отановить туннелирование"),
    # Добавьте здесь любые другие команды, которые вы хотите добавить
]

bot.set_my_commands(commands)

# Список разрешенных ID пользователей
allowed_users = [ВАШ_ID]

# Декоратор для обработчиков сообщений, который проверяет ID пользователя
def restricted(func):
    @wraps(func)
    def wrapped(message):
        if message.from_user.id not in allowed_users:
            bot.send_message(message.chat.id, "Это закрытый бот")
            return
        return func(message)
    return wrapped

# Пример обработчика команды /start с проверкой ID пользователя
@bot.message_handler(commands=['start'])
@restricted
def start_command(message):
    bot.send_message(message.chat.id, " Ngrok tunnel")
    

@bot.message_handler(commands=['ngrok'])
@restricted
def handle_ngrok_command(message):
    # Создаем клавиатуру для выбора протокола и порта
    keyboard = types.InlineKeyboardMarkup()
    http_button = types.InlineKeyboardButton(text="HTTP", callback_data="http")
    tcp_button = types.InlineKeyboardButton(text="TCP", callback_data="tcp")
    keyboard.add(http_button, tcp_button)

    bot.send_message(message.chat.id, "Выберите протокол:", reply_markup=keyboard)

# Обработчик нажатия на кнопки выбора протокола
@bot.callback_query_handler(func=lambda call: call.data in ["http", "tcp"])
@restricted
def handle_protocol_choice(call):
    # Получаем выбранный протокол и отправляем сообщение с просьбой ввести порт
    protocol = call.data
    bot.answer_callback_query(callback_query_id=call.id)
    bot.send_message(call.message.chat.id, f"Введите порт для протокола {protocol}:")

    # Устанавливаем обработчик ввода порта
    bot.register_next_step_handler(call.message, lambda message: handle_port_choice(message, protocol))

# Обработчик ввода порта
def handle_port_choice(message, protocol):
    # Получаем введенный порт и запускаем ngrok
    port = message.text
    ngrok_command = ["ngrok", protocol, port]
    ngrok_process = subprocess.Popen(ngrok_command, stdout=subprocess.PIPE)
    time.sleep(10) # Добавляем задержку в секундах
    tunnel_url = get_tunnel_url()
    #bot.send_message(message.chat.id, f"Ваш туннель: {tunnel_url}")
    bot.send_message(message.chat.id, f"Ваш туннель:\n <code>{tunnel_url}</code>", parse_mode="HTML")

# Обработчик остановки ngrok
@bot.message_handler(commands=['ngrok_stop'])
@restricted
def handle_ngrok_stop_command(message):
    ngrok_process = get_ngrok_process()
    if ngrok_process is not None:
        ngrok_process.terminate()
        bot.send_message(message.chat.id, "Ngrok остановлен")
    else:
        bot.send_message(message.chat.id, "Ngrok не запущен")

# Функция для получения процесса ngrok
def get_ngrok_process():
    for proc in psutil.process_iter():
        try:
            if proc.name() == "ngrok":
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

# Функция для получения URL туннеля
def get_tunnel_url():
    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    data = json.loads(response.text)
    public_url = data["tunnels"][0]["public_url"]
    return public_url

bot.polling()
