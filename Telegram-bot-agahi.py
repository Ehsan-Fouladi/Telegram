import mysql.connector
from config import TOKEN, db_config, channels
from telebot import TeleBot, types
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
import re

state_storage = StateMemoryStorage()
bot = TeleBot(token=TOKEN, state_storage=state_storage, parse_mode="HTML")

chat_ids = []
texts = {}

class Support(StatesGroup):
    text = State()
    respond = State()
    agahi = State()

def escape_special_characters(text):
    special_characters = r"([\*\_\[\]\(\)\~\`\>\#\+\-\=\|\{\}\.\!])"
    return re.sub(special_characters, r'\\\1', text)


def check_joine(user, channels):

    for i in channels:
        is_member = bot.get_chat_member(chat_id=i, user_id=user)

        if is_member.status in ['kicked', 'left']:
            return False

    return True


def user_balance(user):
    sql = f"SELECT balance FROM users WHERE id = {user}"

    with mysql.connector.connect(**db_config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
    return result


@bot.message_handler(commands=['start'])
def send_start(m):
    # markup = types.InlineKeyboardMarkup()
    # button = types.InlineKeyboardButton(
    #     text="عضو شوید", callback_data='proceed')
    # markup.add(button)

    with mysql.connector.connect(**db_config) as connection:
        with connection.cursor() as cursor:
            sql = f"SELECT lang FROM users WHERE id = {m.from_user.id}"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result is None:

                token = m.text.split()
                if len(token) > 1:
                    sql = f"UPDATE users SET balance = balance + 10000 WHERE id = {token[1]}"
                    cursor.execute(sql)
                    connection.commit()

                sql = f"INSERT INTO users (id) VALUES ({m.from_user.id})"
                cursor.execute(sql)
                connection.commit()

                markup = types.InlineKeyboardMarkup(row_width=2)
                button_1 = types.InlineKeyboardButton(text="English", callback_data="eng")
                button_2 = types.InlineKeyboardButton(text="فارسی", callback_data="per")
                markup.add(button_1, button_2)

                bot.send_message(chat_id=m.chat.id, text="کاربر گرامی لطف زبان خودتون را انتخاب کنید؟\n Plase Your Slect Your language", reply_markup=markup)
            else:
                if result[0] == "per":
                    markup_kayboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                    markup_kayboard.add("ثبت اگهی")
                    markup_kayboard.add("حساب کاربری", "شارژ حساب", "زیر مجموعه گیری", "پشتیبانی")

                    bot.send_message(chat_id=m.chat.id, text="به ربات ما خوش آمدید", reply_markup=markup_kayboard)
                else:
                    markup_kayboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                    markup_kayboard.add("Submit ADS")
                    markup_kayboard.add("My account", "Add funds", "Referral", "Support")

                    bot.send_message(
                        chat_id=m.chat.id, text="Welcome To Bot", reply_markup=markup_kayboard)


@bot.message_handler(commands=["languages"])
def change_lang(m):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(text="English", callback_data="eng")
    button_2 = types.InlineKeyboardButton(text="فارسی", callback_data="per")
    markup.add(button_1, button_2)

    bot.send_message(
        chat_id=m.chat.id, text="کاربر گرامی لطف زبان خودتون را انتخاب کنید؟\n Plase Your Slect Your language", reply_markup=markup)


@bot.message_handler(func=lambda m:m.text == "ثبت اگهی")
def get_agahi(m: types.Message):
    bot.send_message(chat_id=m.chat.id, text="حالا آگهی خودت را بفرست")
    bot.set_state(user_id=m.from_user.id, state=Support.agahi, chat_id=m.chat.id)


@bot.message_handler(state=Support.agahi)
def agahi(m: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(text="رد کردن", callback_data="deny")
    button_2 = types.InlineKeyboardButton(text="تایید کردن", callback_data="confirm")
    markup.add(button_1, button_2)

    forwarded = bot.forward_message(chat_id=1857340618, from_chat_id=m.chat.id, message_id=m.message_id)

    bot.send_message(chat_id=1857340618, text=f"این کاربر میخواد اگهی بزاره\n\nایدی کاربر: {m.from_user.id}" , reply_markup=markup, reply_to_message_id=forwarded.message_id)

    bot.send_message(chat_id=m.chat.id, text="آگهی شما تاساعاتی دیگر تایید یا رد میشود؟")
    bot.delete_state(user_id=m.from_user.id, chat_id=m.chat.id)


@bot.callback_query_handler(func=lambda call:call.data == "deny")
def deny(call: types.CallbackQuery):
    pattern = r"ایدی کاربر: \d+"
    user = re.findall(pattern=pattern, string=call.message.text)[0].split()[2]

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="با موفقیت رد شد", callback_data="dadhau8wdhbn")
    markup.add(button)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    bot.send_message(chat_id=int(user), text="درخواست شما رد شد")


@bot.callback_query_handler(func=lambda call:call.data == "confirm")
def confirm(call: types.CallbackQuery):
    pattern = r"ایدی کاربر: \d+"
    user = re.findall(pattern=pattern, string=call.message.text)[0].split()[2]

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="با موفقیت تایید شد.", callback_data="dawdhuhsf")
    markup.add(button)

    bot.copy_message(chat_id="id channel", from_chat_id=call.message.chat.id, message_id=call.message.reply_to_message.message_id)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    bot.send_message(chat_id=int(user), text="آگهی شما ثبت شد")


@bot.message_handler(func=lambda m: m.text == "حساب کاربری")
def account(m):
    balance = user_balance(user=m.from_user.id)

    text = f"""اطلاعات حساب کاربری شما:
            نام کاربری: <a href='tg://user?id={m.from_user.id}'>{m.from_user.username}</a>
            شناسه کاربری: <code>{m.from_user.id}</code>
            موجودی: {balance[0]} تومان
            """

    bot.send_message(chat_id=m.chat.id, text=text)


@bot.message_handler(func=lambda m: m.text == "زیر مجموعه گیری")
def referral(m):
    with open("./ghost.jpg", "rb") as photo:
        bot.send_photo(m.chat.id, photo=photo, caption=f"""این لینک رفرال شما است : 
                       
                       https://t.me/AdvertisingShopBot?start={m.from_user.id}""")


@bot.message_handler(func=lambda m: m.text == "پشتیبانی")
def sup(m):
    bot.send_message(chat_id=m.chat.id, text="لطفا پیام خودتون را وارد کنید!")
    bot.set_state(user_id=m.from_user.id, state=Support.text, chat_id=m.chat.id)


@bot.message_handler(state=Support.text)
def sup_text(m):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text="پاسخ", callback_data=m.from_user.id)
    markup.add(button)

    bot.send_message(chat_id=1857340618, text=f"Recived a message from <code>{m.from_user.id}</code> with username @{m.from_user.username}:\n\nMessage text:\n<b>{escape_special_characters(m.text)}</b>", reply_markup=markup)

    bot.send_message(chat_id=m.chat.id, text="Your message was sent!")

    texts[m.from_user.id] = m.text

    bot.delete_state(user_id=m.from_user.id, chat_id=m.chat.id)


@bot.message_handler(state=Support.respond)
def answer_text(m):
    chat_id = chat_ids[-1]

    if chat_id in texts:
        bot.send_message(
            chat_id=chat_id, text=f"Your massage:\n<i>{escape_special_characters(texts[chat_id])}</i>\n\n Support answer:\n<b>{escape_special_characters(m.text)}</b>")
        bot.send_message(chat_id=m.chat.id, text="Your answer was sent")

        del texts[chat_id]
        chat_ids.remove(chat_id)
    else:
        bot.send_message(chat_id=m.chat.id, text="Something went wrong. Please try again")
    bot.delete_state(user_id=m.from_user.id, chat_id=m.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "eng")
def english(call):
    with mysql.connector.connect(**db_config) as connection:
        with connection.cursor() as cursor:
            sql = f"UPDATE users SET lang = 'eng' WHERE id = {call.from_user.id}"
            cursor.execute(sql)
            connection.commit()

    markup_kayboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup_kayboard.add("Submit ADS")
    markup_kayboard.add("My account ", "Add funds", "Referral", "Support")

    bot.send_message(chat_id=call.message.chat.id, text="Your Language is English", reply_markup=markup_kayboard)


@bot.callback_query_handler(func=lambda call: call.data == "per")
def pershan(call):
    with mysql.connector.connect(**db_config) as connection:
        with connection.cursor() as cursor:
            sql = f"UPDATE users SET lang = 'per' WHERE id = {call.from_user.id}"
            cursor.execute(sql)
            connection.commit()

    markup_kayboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup_kayboard.add("ثبت اگهی")
    markup_kayboard.add("حساب کاربری", "شارژ حساب","زیر مجموعه گیری", "پشتیبانی")

    bot.send_message(chat_id=call.message.chat.id, text="زبان شما فارسی است", reply_markup=markup_kayboard)


@bot.callback_query_handler(func=lambda call: call.data == "proceed")
def proceed(call):
    is_member = check_joine(user=call.from_user.id, channels=channels)
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="تایید", callback_data='proceed')
    markup.add(button)

    if is_member is False:
        bot.send_message(chat_id=call.message.chat.id, text="در کانال ما جوین شوید؟", reply_markup=markup)
    else:
        bot.send_message(chat_id=call.message.chat.id, text="شما میتوانید از ربات استفاده کنید.")


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    bot.send_message(chat_id=call.message.chat.id, text=f"Send your answer to <code>{call.data}</code>:")

    chat_ids.append(int(call.data))

    bot.set_state(user_id=call.from_user.id, state=Support.respond, chat_id=call.message.chat.id)

# Payment gateway

# @bot.message_handler(func=lambda m:m.text == "شارژ حساب")
# def change_account(m):
#     markup = types.InlineKeyboardMarkup()
#     button_1 = types.InlineKeyboardButton(text="10 تومان", callback_data="stat")
#     markup.add(button_1)
#     bot.send_message(m.chat.id, text="مقدار شارژ خود را انتخاب کنید.", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call:call.data == "stat")
# def thouands(call):
#     markup = types.InlineKeyboardMarkup()
#     button = types.InlineKeyboardButton(text="پرداخت", url="https://codeyad.com/")
#     markup.add(button)
#     bot.send_message(call.message.chat.id, text="از این لینک پرداخت کنید.", reply_markup=markup)

if __name__ == "__main__":
    bot.set_my_commands([
        types.BotCommand("/start", "Start Bot"),
        types.BotCommand("/languages", "Slect Language"),
    ])
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
