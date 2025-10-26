from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards import get_currency_keyboard
from converter import rub_to_usd, usd_to_rub, USD  # Теперь импортируем USD вместо USD_RATE

# Создаем роутер - это главный объект для обработки сообщений
router = Router()
#Router - помощник который направляет сообщения в нужные функции
#Handler - функция которая обрабатывает определенные сообщения

# Словарь для запоминания что хочет сделать каждый пользователь, чтобы бот помнил кому на какое сообщение как отвечать
user_states = {}

@router.message(CommandStart())
async def start_command(message: Message):
    #Обрабатывает команду /start
    print(f"Пользователь {message.from_user.id} написал /start")  # Для отладки
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n" #Приветствие и имя пользователя
        "Я бот для конвертации валют.\n"
        "Выбери действие:",
        reply_markup=get_currency_keyboard()
    )

@router.message(Command('help'))
async def help_command(message: Message):
    #Обрабатывает команду /help
    help_text = """
Как пользоваться ботом:

- Нажми "Рубли в Доллары" и введи сумму в рублях
- Нажми "Доллары в Рубли" и введи сумму в долларах  
- "Текущий курс" - покажет актуальный курс USD/RUB"""
    await message.answer(help_text, reply_markup=get_currency_keyboard())

@router.message(F.text == "Текущий курс")
async def show_rate(message: Message):
    #Показывает текущий курс доллара
    await message.answer(f"Текущий курс: 1 USD = {USD} RUB")

@router.message(F.text == "Помощь")
async def show_help(message: Message):
    #Показывает справку
    await help_command(message)

@router.message(F.text == "Рубли в Доллары")
async def rub_to_usd_handler(message: Message):
    #Обрабатывает выбор конвертации рублей в доллары
    user_states[message.from_user.id] = "waiting_rub_amount"
    await message.answer("Введите сумму в рублях:")

@router.message(F.text == "Доллары в Рубли")
async def usd_to_rub_handler(message: Message):
   #Обрабатывает выбор конвертации долларов в рубли
    user_states[message.from_user.id] = "waiting_usd_amount"
    await message.answer("Введите сумму в долларах:")

@router.message()
async def handle_amount(message: Message):
    #Обрабатывает ввод сумм для конвертации
    user_id = message.from_user.id
    state = user_states.get(user_id)
    
    try:
        amount = float(message.text)
        
        if state == "waiting_rub_amount":
            result = rub_to_usd(amount)
            await message.answer(f"{amount} RUB = {result} USD\nПо курсу: 1 USD = {USD} RUB")
            user_states[user_id] = None
            
        elif state == "waiting_usd_amount":
            result = usd_to_rub(amount)
            await message.answer(f"{amount} USD = {result} RUB\nПо курсу: 1 USD = {USD} RUB")
            user_states[user_id] = None
            
        else:
            await message.answer("Выберите действие с помощью кнопок ниже", reply_markup=get_currency_keyboard())
            
    except ValueError:
        await message.answer("Пожалуйста, введите число!")