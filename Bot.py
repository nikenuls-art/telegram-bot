from flask import Flask
from threading import Thread
import os

TOKEN = "8514273761:AAH3YeenOrWomYPUZve9NadLfwLB1py9P18"
ADMIN_ID = 8504692404

REVIEWS_LINK = "https://t.me/SanyaRysel"
SUPPORT_USERNAME = "@veryselov"

bot = telebot.TeleBot(TOKEN)

user_data = {}
user_step = {}

order_id = 1
orders = {}

# ================= VALIDATION =================

def is_valid_gmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email, re.IGNORECASE)

# ================= PRICE =================

def calculate_price(subs):

    subs = int(subs)

    if 1 <= subs <= 10:
        return "25 сом"

    elif 10 < subs <= 50:
        return "30 сом"

    elif 50 < subs <= 100:
        return "40 сом"

    elif 100 < subs <= 200:
        return "50 сом"

    elif 200 < subs <= 350:
        return "75 сом"

    elif 350 < subs <= 500:
        return "90 сом"

    elif 500 < subs <= 650:
        return "120 сом"

    elif 650 < subs <= 800:
        return "150 сом"

    elif 800 < subs <= 1000:
        return "200 сом"

    elif 1000 < subs <= 1300:
        return "250 сом"

    elif 1300 < subs <= 1500:
        return "300 сом"

    elif 1500 < subs <= 1750:
        return "350 сом"

    elif 1750 < subs <= 2000:
        return "450 сом"

    elif 2000 < subs <= 3000:
        return "750 сом"

    elif 3000 < subs <= 5000:
        return "900 сом"

    elif 5000 < subs <= 10000:
        return "1.5K сом"

    elif 10000 < subs <= 25000:
        return "2K сом"

    elif 25000 < subs <= 50000:
        return "3K сом"

    else:
        return "Договорная"

# ================= MENU =================

def send_main_menu(chat_id):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    sell_btn = types.KeyboardButton("💸 Продать канал")
    reviews_btn = types.KeyboardButton("⭐ Отзывы")
    support_btn = types.KeyboardButton("🛠 Поддержка")
    status_btn = types.KeyboardButton("📦 Статус заказа")

    markup.row(sell_btn)
    markup.row(reviews_btn, support_btn)
    markup.row(status_btn)

    text = """
🔥 RySell Shop

💎 Скупка YouTube/TikTok каналов
⚡ Быстрые выплаты
🛡 Поддержка 24/7

👇 Выберите действие ниже
"""

    bot.send_message(chat_id, text, reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    send_main_menu(message.chat.id)

# ================= MENU BUTTON =================

@bot.message_handler(func=lambda m: m.text == "🏠 Меню")
def menu_handler(message):
    send_main_menu(message.chat.id)

# ================= STATUS =================

@bot.message_handler(func=lambda m: m.text == "📦 Статус заказа")
def order_status(message):

    user_id = message.from_user.id

    result = []

    for order_num, data in orders.items():

        if data["user_id"] == user_id:

            result.append(
                f"""📦 Заказ #{order_num}

📌 Статус: {data['status']}"""
            )

    if not result:

        bot.send_message(
            message.chat.id,
            "❌ У вас нет заказов"
        )

        return

    bot.send_message(
        message.chat.id,
        "\n\n".join(result)
    )

# ================= REVIEWS =================

@bot.message_handler(func=lambda m: m.text == "⭐ Отзывы")
def reviews(message):

    bot.send_message(
        message.chat.id,
        f"⭐ Отзывы:\n\n{REVIEWS_LINK}"
    )

# ================= SUPPORT =================

@bot.message_handler(func=lambda m: m.text == "🛠 Поддержка")
def support(message):

    bot.send_message(
        message.chat.id,
        f"🛠 Поддержка:\n\n{SUPPORT_USERNAME}"
    )

# ================= SELL =================

@bot.message_handler(func=lambda m: m.text == "💸 Продать канал")
def sell(message):

    user_data[message.chat.id] = {}

    ask_region(message.chat.id)

# ================= BACK MARKUP =================

def back_markup():

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    back_btn = types.KeyboardButton("⬅️ Назад")
    menu_btn = types.KeyboardButton("🏠 Меню")

    markup.row(back_btn, menu_btn)

    return markup

# ================= ASK =================

def ask_region(chat_id):

    user_step[chat_id] = "region"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(
        types.KeyboardButton("🇺🇸 USA"),
        types.KeyboardButton("🇷🇺 Russia")
    )

    markup.row(
        types.KeyboardButton("🌍 Другое")
    )

    markup.row(
        types.KeyboardButton("⬅️ Назад"),
        types.KeyboardButton("🏠 Меню")
    )

    bot.send_message(
        chat_id,
        "🌍 Укажите регион канала",
        reply_markup=markup
    )

def ask_subs(chat_id):

    user_step[chat_id] = "subs"

    bot.send_message(
        chat_id,
        "👥 Сколько подписчиков на канале?",
        reply_markup=back_markup()
    )

def ask_content(chat_id):

    user_step[chat_id] = "content"

    bot.send_message(
        chat_id,
        "🎬 Какой контент на канале?",
        reply_markup=back_markup()
    )

def ask_login(chat_id):

    user_step[chat_id] = "login"

    bot.send_message(
        chat_id,
        """📧 Отправьте Gmail от канала

Пример:
example@gmail.com""",
        reply_markup=back_markup()
    )

def ask_password(chat_id):

    user_step[chat_id] = "password"

    bot.send_message(
        chat_id,
        """🔑 Отправьте пароль от канала""",
        reply_markup=back_markup()
    )

def ask_bank(chat_id):

    user_step[chat_id] = "bank"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(
        types.KeyboardButton("🟢 Mbank"),
        types.KeyboardButton("🔵 Bakai Bank")
    )

    markup.row(
        types.KeyboardButton("🟡 O! Деньги"),
        types.KeyboardButton("⚫ VISA")
    )

    markup.row(
        types.KeyboardButton("⬅️ Назад"),
        types.KeyboardButton("🏠 Меню")
    )

    bot.send_message(
        chat_id,
        "🏦 Куда вывести оплату?",
        reply_markup=markup
    )

def ask_method(chat_id):

    bank = user_data[chat_id]["bank"]

    # VISA
    if bank == "⚫ VISA":

        user_step[chat_id] = "payment"
        user_data[chat_id]["method"] = "💳 VISA"

        bot.send_message(
            chat_id,
            "💳 Отправьте номер VISA карты",
            reply_markup=back_markup()
        )

        return

    user_step[chat_id] = "method"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(
        types.KeyboardButton("📱 По номеру телефона"),
        types.KeyboardButton("💳 По номеру карты")
    )

    markup.row(
        types.KeyboardButton("📷 QR-код")
    )

    markup.row(
        types.KeyboardButton("⬅️ Назад"),
        types.KeyboardButton("🏠 Меню")
    )

    bot.send_message(
        chat_id,
        "💸 Как получить деньги?",
        reply_markup=markup
    )

def ask_payment(chat_id, method):

    user_step[chat_id] = "payment"

    if method == "📱 По номеру телефона":

        bot.send_message(
            chat_id,
            "📱 Отправьте номер телефона",
            reply_markup=back_markup()
        )

    elif method == "💳 По номеру карты":

        bot.send_message(
            chat_id,
            "💳 Отправьте номер карты",
            reply_markup=back_markup()
        )

    elif method == "📷 QR-код":

        bot.send_message(
            chat_id,
            "📷 Отправьте QR-код фото",
            reply_markup=back_markup()
        )

# ================= CALLBACKS =================

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    data = call.data

    if data.startswith("accept_"):

        order_num = int(data.split("_")[1])

        if order_num in orders:

            orders[order_num]["status"] = "✅ Оплачено"

            user_id = orders[order_num]["user_id"]

            bot.send_message(
                user_id,
                f"""✅ Ваша заявка #{order_num} оплачена"""
            )

            bot.answer_callback_query(
                call.id,
                "Оплачено"
            )

    elif data.startswith("decline_"):

        order_num = int(data.split("_")[1])

        if order_num in orders:

            orders[order_num]["status"] = "❌ Отказано"

            user_id = orders[order_num]["user_id"]

            bot.send_message(
                user_id,
                f"""❌ Ваша заявка #{order_num} отклонена"""
            )

            bot.answer_callback_query(
                call.id,
                "Отклонено"
            )

# ================= MAIN =================

@bot.message_handler(content_types=['text', 'photo'])
def all_messages(message):

    global order_id

    chat_id = message.chat.id

    if message.content_type == "text":
        text = message.text
    else:
        text = ""

    if text == "🏠 Меню":
        send_main_menu(chat_id)
        return

    if chat_id not in user_step:
        return

    step = user_step[chat_id]

    # ================= BACK =================

    if text == "⬅️ Назад":

        if step == "subs":
            ask_region(chat_id)

        elif step == "content":
            ask_subs(chat_id)

        elif step == "login":
            ask_content(chat_id)

        elif step == "password":
            ask_login(chat_id)

        elif step == "bank":
            ask_password(chat_id)

        elif step == "method":
            ask_bank(chat_id)

        elif step == "payment":

            if user_data[chat_id]["bank"] == "⚫ VISA":
                ask_bank(chat_id)
            else:
                ask_method(chat_id)

        return

    # ================= REGION =================

    if step == "region":

        user_data[chat_id]["region"] = text

        ask_subs(chat_id)

    # ================= SUBS =================

    elif step == "subs":

        if not text.isdigit():

            bot.send_message(
                chat_id,
                "❌ Введите только цифры"
            )

            return

        user_data[chat_id]["subs"] = text

        price = calculate_price(text)

        user_data[chat_id]["price"] = price

        bot.send_message(
            chat_id,
            f"""💰 Примерная цена канала: {price}

⚠️ Цена зависит от:
• Активности
• Просмотров
• Тематики
• Страны аудитории"""
        )

        ask_content(chat_id)

    # ================= CONTENT =================

    elif step == "content":

        user_data[chat_id]["content"] = text

        ask_login(chat_id)

    # ================= LOGIN =================

    elif step == "login":

        if not is_valid_gmail(text):

            bot.send_message(
                chat_id,
                "❌ Отправьте только Gmail"
            )

            return

        user_data[chat_id]["login"] = text

        ask_password(chat_id)

    # ================= PASSWORD =================

    elif step == "password":

        user_data[chat_id]["password"] = text

        ask_bank(chat_id)

    # ================= BANK =================

    elif step == "bank":

        user_data[chat_id]["bank"] = text

        ask_method(chat_id)

    # ================= METHOD =================

    elif step == "method":

        user_data[chat_id]["method"] = text

        ask_payment(chat_id, text)

    # ================= PAYMENT =================

    elif step == "payment":

        payment_data = ""

        if message.content_type == "photo":

            payment_data = "📷 QR-код"

        else:

            payment_data = text

        user_data[chat_id]["payment"] = payment_data

        orders[order_id] = {
            "user_id": chat_id,
            "status": "⏳ На проверке"
        }

        markup = types.InlineKeyboardMarkup()

        accept_btn = types.InlineKeyboardButton(
            "✅ Оплатить",
            callback_data=f"accept_{order_id}"
        )

        decline_btn = types.InlineKeyboardButton(
            "❌ Отказать",
            callback_data=f"decline_{order_id}"
        )

        markup.row(accept_btn, decline_btn)

        admin_text = f"""
📦 Заявка #{order_id}

🌍 Регион: {user_data[chat_id]['region']}
👥 Подписчики: {user_data[chat_id]['subs']}
💰 Цена: {user_data[chat_id]['price']}
🎬 Контент: {user_data[chat_id]['content']}

📧 Gmail: {user_data[chat_id]['login']}
🔑 Пароль: {user_data[chat_id]['password']}

🏦 Банк: {user_data[chat_id]['bank']}
💸 Способ выплаты: {user_data[chat_id]['method']}

💳 Данные:
{user_data[chat_id]['payment']}

📌 Статус: ⏳ На проверке
"""

        if message.content_type == "photo":

            file_id = message.photo[-1].file_id

            bot.send_photo(
                ADMIN_ID,
                file_id,
                caption=admin_text,
                reply_markup=markup
            )

        else:

            bot.send_message(
                ADMIN_ID,
                admin_text,
                reply_markup=markup
            )

        bot.send_message(
            chat_id,
            f"""✅ Заявка #{order_id} отправлена

📌 Статус: ⏳ На проверке"""
        )

        order_id += 1

        user_step.pop(chat_id, None)
        user_data.pop(chat_id, None)

print("Бот запущен")


from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

bot.infinity_polling(skip_pending=True)
