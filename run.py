import asyncio
import logging
from aiogram import Bot, Dispatcher #Bot - ваш бот в Telegram, как бы "аккаунт" бота
from handlers import router #Dispatcher - главный управляющий, который решает что делать с сообщениями
#async/await - специальные слова которые помогают боту работать быстро с многими пользователями
def load_bot_token():

    #Читает токен бота из файла config.env

    try:
        with open('config.env', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('BOT_TOKEN='):
                    token = line.split('=', 1)[1] #строчка говорит что мы после равно в файле env берем всю строчку
                    if token:  # проверяем что токен не пустой
                        print(f"Токен загружен: {token[:10]}...")
                        return token
                    else:
                        print("У вас отсутствует токен или он введен неверно!")
                        return None
    except FileNotFoundError:
        print("Файл config.env не найден!")
        return None
    
    print("ОШИБКА: BOT_TOKEN не найден в config.env!")
    return None

#главная функция программы (main)
async def main():

    print("Запускаем бота...")
    
    BOT_TOKEN = load_bot_token()
    if not BOT_TOKEN:
        return
    
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("=== Бот-конвертер валют ЗАПУЩЕН! ===")
    print("Откройте Telegram и напишите /start")
    print("Для остановки нажмите Ctrl+C")
    print("-" * 50)

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("\nОстанавливаем бота...")
    finally:
        await bot.session.close()
        print("Бот остановлен")
#базовая конструкция запуска через main для python
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершила работу")