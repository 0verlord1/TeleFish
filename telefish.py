from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import json, os, time

def clear():
    if os.name == "nt":  # Если Windows
        os.system("cls")
    else:  # Если macOS или Linux
        os.system("clear")

def enter():
    print('''Главное меню!
1. Запуск
2. Настройки
3. Выход''')
    number = input('Введите функцию: ')
    return number

def load_config(filename="config.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"api": "", "text": "", "text_button": ""}

def save_config(api, text, text_button, filename="config.json"):
    config = {
        "api": api,
        "text": text,
        "text_button": text_button
    }
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)
    print(f"Конфигурация сохранена в {filename}")
    time.sleep(3)

while True:
    clear()
    ent = enter()
    if ent == '1':
        clear()
        config_data = load_config()

        if not config_data["api"] or not config_data["text"] or not config_data["text_button"]:
            print("Настройки не найдены или неполные. Пожалуйста, введите данные.")
            config_data["api"] = input("Введите API токен: ")
            clear()
            print('Текст приветствия по умолчанию = \'Для использования нашего бота вас нужно идентифицировать\'')
            config_data["text"] = input("Нажмите Enter чтобы оставить по умолчанию: ")
            if config_data["text"] == '':
                config_data["text"] = 'Для использования нашего бота вас нужно идентифицировать'
            clear()
            print('Текст кнопки по умолчанию = \'Поделиться номером\'')
            config_data["text_button"] = input("Нажмите Enter чтобы оставить по умолчанию: ")
            if config_data["text_button"] == '':
                config_data["text_button"] = 'Поделиться номером'
            clear()
            # Сохраняем данные в конфигурационный файл
            save_config(config_data["api"], config_data["text"], config_data["text_button"])
            clear()

        api, text, text_button = config_data["api"], config_data["text"], config_data["text_button"]
        try:
            bot = Bot(api)
            dp = Dispatcher(bot)
            print('Извините, но такого API ключа не существует!')
            @dp.message_handler(content_types=types.ContentType.CONTACT)
            async def process_contact(message: types.Message):
                if message.contact.user_id == message.from_user.id:
                    # Номер телефона принадлежит пользователю
                    await message.answer(f"Спасибо! Ваш номер телефона: {message.contact.phone_number}", reply_markup=ReplyKeyboardRemove())
                    print(message.contact.phone_number)
                else:
                    # Номер телефона отправлен от другого пользователя
                    await message.answer("Кажется, это не ваш номер телефона!")
            
            @dp.message_handler()
            async def start(message: types.Message):
                keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                phone_button = KeyboardButton(text=text_button, request_contact=True)
                keyboard.add(phone_button)
                await message.answer(text, reply_markup=keyboard)
        
            executor.start_polling(dp, skip_updates=True)
        except:
            print('Извините, но такого API ключа не существует!')
            time.sleep(3)

    elif ent == '2':
        clear()
        print("Настройки:")
        api, text, text_button = load_config().values()
        print(f"API: {api}")
        print(f"Текст: {text}")
        print(f"Текст кнопки: {text_button}")
        input("Нажмите Enter чтобы продолжить: ")
    elif ent == '3':
        break
    else:
        clear()
        print('Такой функции нет, Выберите цифру из меню!')
        input('Нажмите Enter чтобы продолжить: ')