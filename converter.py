def load_config():
    #Читает файл config.env и возвращает настройки
    config = {}
    try:
        with open('config.env', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value
    except FileNotFoundError:
        print("Файл config.env не найден!")
        return {}
    return config

# Загружаем настройки
config = load_config()

# Получаем курс доллара (теперь переменная называется USD)
USD = float(config.get('USD', '80.0'))  # Значение по умолчанию 80

print(f"Курс доллара установлен: {USD}")  # Для отладки

def rub_to_usd(rub_amount):
    #Конвертирует рубли в доллары
    usd_amount = rub_amount / USD
    return round(usd_amount, 2)

def usd_to_rub(usd_amount):
    #Конвертирует доллары в рубли
    rub_amount = usd_amount * USD
    return round(rub_amount, 2)