# Скрипт управления Ngrok через Telegram

1. Устанавливаем и настраиваем [ngrok](https://ngrok.com/download)
2. Устанавливаем недостающие библиотеки

        pip install telebot subprocess requests psutil

3. Идём в телеграм-бота [BotFather](https://t.me/BotFather), создаём бота и получаем токен.
4. Вставляем токен в строку:

        bot = telebot.TeleBot('ТОКЕН_ВАШЕГО_БОТА')
5. Имеется ограничение доступа по id пользователя:
    1. Идем в [этот](https://t.me/MissRose_bot) бот и пишем

            /id
    2. вставляем свой id в этой строке:

            allowed_users = [ВАШ_ID]
        
        Можно добавить несколько через запятую

6. Запускаем и проверяем

    ![start](https://user-images.githubusercontent.com/24943522/240642513-3effff10-8fcd-45e1-81cd-f31fd97211b7.jpg)

## Особенности бота
* Есть меню команд  

    ![menu](https://user-images.githubusercontent.com/24943522/240642521-3249e660-2ee8-45b7-8519-fc0bafeab499.jpg)
* Доступно на выбор TCP и HTTP/S

    ![http](https://user-images.githubusercontent.com/24943522/240642500-12d111c7-660d-4250-9483-ba87bde1ab0c.jpg)

    ![tcp](https://user-images.githubusercontent.com/24943522/240642509-5c5225ff-5b16-4cc7-a837-d50f891f34a7.jpg)