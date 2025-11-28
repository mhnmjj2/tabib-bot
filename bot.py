import telebot
from telebot import types

from vip.activate import activate_vip, is_admin
from vip.check import is_vip
from vip.analysis import advanced_analysis

from questions import questions  # لیست ۵۰ سؤال

BOT_TOKEN = "8505257280:AAEdiMlY75oOiFb26f0zkv4EW3I94agfLgU"
bot = telebot.TeleBot(BOT_TOKEN)

# ذخیره وضعیت آزمون کاربران
user_state = {}
user_scores = {}

# -----------------------------
# ✅ شروع ربات
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("شروع آزمون", "نسخه VIP")

    bot.send_message(
        user_id,
        "سلام! خوش اومدی 🌿\n\nبرای شروع آزمون مزاج‌شناسی، روی «شروع آزمون» بزن.",
        reply_markup=markup
    )


# -----------------------------
# ✅ شروع آزمون
# -----------------------------
@bot.message_handler(func=lambda m: m.text == "شروع آزمون")
def start_test(message):
    user_id = message.chat.id

    user_state[user_id] = 0
    user_scores[user_id] = []

    send_question(user_id)


def send_question(user_id):
    index = user_state[user_id]

    if index >= len(questions):
        finish_test(user_id)
        return

    q = questions[index]

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("خیلی زیاد", callback_data="3"),
        types.InlineKeyboardButton("زیاد", callback_data="2"),
        types.InlineKeyboardButton("متوسط", callback_data="1"),
        types.InlineKeyboardButton("کم", callback_data="0")
    )

    bot.send_message(user_id, f"❓ {q}", reply_markup=markup)


# -----------------------------
# ✅ دریافت پاسخ هر سؤال
# -----------------------------
@bot.callback_query_handler(func=lambda call: call.data in ["0", "1", "2", "3"])
def answer_question(call):
    user_id = call.message.chat.id
    score = int(call.data)

    user_scores[user_id].append(score)
    user_state[user_id] += 1

    send_question(user_id)


# -----------------------------
# ✅ پایان آزمون و محاسبه مزاج
# -----------------------------
def finish_test(user_id):
    scores = user_scores[user_id]

    warm = sum(scores[0:12]) * 3
    cold = sum(scores[12:25]) * 3
    dry = sum(scores[25:38]) * 3
    wet = sum(scores[38:50]) * 3

    total = warm + cold + dry + wet

    result = {
        "warm": int((warm / total) * 100),
        "cold": int((cold / total) * 100),
        "dry": int((dry / total) * 100),
        "wet": int((wet / total) * 100)
    }

    # ذخیره نتیجه برای VIP
    user_scores[user_id] = result

    # پیام نتیجه ساده
    bot.send_message(
        user_id,
        f"✅ آزمون شما تمام شد!\n\n"
        f"🌡️ گرمی: {result['warm']}٪\n"
        f"❄️ سردی: {result['cold']}٪\n"
        f"🌵 خشکی: {result['dry']}٪\n"
        f"💧 تری: {result['wet']}٪\n\n"
        f"برای دریافت تحلیل کامل VIP، روی دکمه زیر بزن."
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("فعال‌سازی VIP", callback_data="buy_vip"))

    bot.send_message(user_id, "🌟 نسخه VIP شامل تحلیل کامل مزاج شماست.", reply_markup=markup)


# -----------------------------
# ✅ دکمه فعال‌سازی VIP
# -----------------------------
@bot.callback_query_handler(func=lambda call: call.data == "buy_vip")
def buy_vip(call):
    user_id = call.message.chat.id

    bot.send_message(
        user_id,
        "برای فعال‌سازی VIP، لطفاً رسید پرداخت را ارسال کنید.\n"
        "پس از ارسال رسید، مدیر آن را بررسی و تأیید می‌کند 🌿"
    )


# -----------------------------
# ✅ دریافت رسید پرداخت
# -----------------------------
@bot.message_handler(content_types=['photo'])
def receive_receipt(message):
    user_id = message.chat.id

    # ارسال پیام به مدیر
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ تأیید VIP", callback_data=f"approve_{user_id}"),
        types.InlineKeyboardButton("❌ رد", callback_data=f"reject_{user_id}")
    )

    bot.send_message(
        6271244163,
        f"کاربر {user_id} رسید پرداخت ارسال کرد.\nآیا تأیید می‌کنید؟",
        reply_markup=markup
    )

    bot.send_message(user_id, "رسید شما ارسال شد ✅\nمنتظر تأیید مدیر باشید.")


# -----------------------------
# ✅ تأیید VIP توسط مدیر
# -----------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_vip(call):
    if not is_admin(call.message.chat.id):
        return

    user_id = int(call.data.split("_")[1])

    expire = activate_vip(user_id)

    bot.send_message(user_id, f"🎉 VIP شما فعال شد!\nتاریخ انقضا: {expire}")
    bot.send_message(call.message.chat.id, "✅ VIP فعال شد.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_"))
def reject_vip(call):
    if not is_admin(call.message.chat.id):
        return

    user_id = int(call.data.split("_")[1])
    bot.send_message(user_id, "❌ پرداخت شما تأیید نشد.")
    bot.send_message(call.message.chat.id, "پرداخت رد شد.")


# -----------------------------
# ✅ دستور مخفی /vip برای مدیر
# -----------------------------
@bot.message_handler(commands=['vip'])
def manual_vip(message):
    if not is_admin(message.chat.id):
        return

    try:
        user_id = int(message.text.split()[1])
        expire = activate_vip(user_id)
        bot.send_message(user_id, f"🎉 VIP شما فعال شد!\nتاریخ انقضا: {expire}")
        bot.send_message(message.chat.id, "✅ VIP فعال شد.")
    except:
        bot.send_message(message.chat.id, "فرمت دستور اشتباه است.")


# -----------------------------
# ✅ دکمه نسخه VIP
# -----------------------------
@bot.message_handler(func=lambda m: m.text == "نسخه VIP")
def vip_section(message):
    user_id = message.chat.id

    if not is_vip(user_id):
        bot.send_message(
            user_id,
            "❌ شما VIP نیستید.\nبرای فعال‌سازی VIP رسید پرداخت را ارسال کنید."
        )
        return

    result = user_scores.get(user_id)

    if not result:
        bot.send_message(user_id, "ابتدا آزمون را انجام دهید.")
        return

    text = advanced_analysis(result)
    bot.send_message(user_id, text)


# -----------------------------
# ✅ اجرای ربات
# -----------------------------
bot.infinity_polling()
