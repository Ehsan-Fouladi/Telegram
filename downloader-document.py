from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import Message, CallbackQuery
from urllib import request
import os

TOKEN = "6451159023:AAG1H57iz-Ql9TCFUcjkOwQSryA99eT1Y3o"

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=["start"])
def start(m: Message):
    bot.send_chat_action(chat_id=m.chat.id, action="typing")
    bot.send_message(chat_id=m.chat.id, text=f"{m.from_user.first_name}\n سلام کاربر گرامی لطف جهت دانلود فایل خود \n /download \n کلیک کنید یا تایپ کنید.")

@bot.message_handler(commands=["help"])
def help(m: Message):
    bot.send_message(chat_id=m.chat.id, text="برای کمک یا دریافت راهنمایی به این به پشتیبانی ما اطلاع دهید. \n @ehsanfouladiprogrammer")

@bot.message_handler(commands=["download"])
def download(m: Message):
    bot.send_chat_action(chat_id=m.chat.id, action="typing")
    bot.send_message(chat_id=m.chat.id, text="لطف لینک ارسال کنید.")

@bot.message_handler(func=lambda m:True)
def sned_link(m: Message):
    bot.send_chat_action(chat_id=m.chat.id, action="typing")
    
    if m.text != m.text.split("https://")[0] or m.text != m.text.split("http://")[0]:
        markup = InlineKeyboardMarkup(row_width=1)
        button_1 = InlineKeyboardButton(text="document.pdf", callback_data="download_1")
        button_2 = InlineKeyboardButton(text="document.doc", callback_data="download_2")
        button_3 = InlineKeyboardButton(text="document.docx", callback_data="download_3")
        button_4 = InlineKeyboardButton(text="document.ppt", callback_data="download_4")
        button_5 = InlineKeyboardButton(text="document.pptx", callback_data="download_5")
        button_6 = InlineKeyboardButton(text="document.xls", callback_data="download_6")
        button_7 = InlineKeyboardButton(text="document.txt", callback_data="download_7")
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, row_width=3)

        doucment_links = m.text

        bot.send_message(chat_id=m.chat.id, text=doucment_links, reply_markup=markup, disable_web_page_preview=True)
    else:
        bot.send_message(chat_id=m.chat.id, text="لطف لینک درست را وارد کنید.")

@bot.callback_query_handler(func=lambda call:call.data == "download_1")
def download_pdf(call: CallbackQuery):
    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_document")
    remote_url = call.message.text
    local_file = 'document.pdf'
    request.urlretrieve(remote_url, local_file)
    bot.send_document(chat_id=call.message.chat.id, document=open("./document.pdf", "rb"))
    bot.send_message(chat_id=call.message.chat.id, text="دانلود با موفقیت انجام شد.")
    os.remove("./document.pdf")

@bot.callback_query_handler(func=lambda call:call.data == "download_2")
def download_doc(call: CallbackQuery):
    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_document")
    remote_url = call.message.text
    local_file = 'document.doc'
    request.urlretrieve(remote_url, local_file)
    bot.send_document(chat_id=call.message.chat.id, document=open("./document.doc", "rb"))
    bot.send_message(chat_id=call.message.chat.id, text="دانلود با موفقیت انجام شد.")
    os.remove("./document.doc")

@bot.callback_query_handler(func=lambda call:call.data == "download_3")
def download_docx(call: CallbackQuery):
    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_document")
    remote_url = call.message.text
    local_file = 'document.docx'
    request.urlretrieve(remote_url, local_file)
    bot.send_document(chat_id=call.message.chat.id, document=open("./document.docx", "rb"))
    bot.send_message(chat_id=call.message.chat.id, text="دانلود با موفقیت انجام شد.")
    os.remove("./document.docx")

@bot.callback_query_handler(func=lambda call:call.data == "download_4")
def download_ppt(call: CallbackQuery):
    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_document")
    remote_url = call.message.text
    local_file = 'document.ppt'
    request.urlretrieve(remote_url, local_file)
    bot.send_document(chat_id=call.message.chat.id, document=open("./document.ppt", "rb"))
    bot.send_message(chat_id=call.message.chat.id, text="دانلود با موفقیت انجام شد.")
    os.remove("./document.ppt")

@bot.callback_query_handler(func=lambda call:call.data == "download_5")
def download_pptx(call: CallbackQuery):
    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_document")
    remote_url = call.message.text
    local_file = 'document.pptx'
    request.urlretrieve(remote_url, local_file)
    bot.send_document(chat_id=call.message.chat.id, document=open("./document.pptx", "rb"))
    bot.send_message(chat_id=call.message.chat.id, text="دانلود با موفقیت انجام شد.")
    os.remove("./document.pptx")

@bot.callback_query_handler(func=lambda call:call.data == "download_6")
def download_xls(call: CallbackQuery):
    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_document")
    remote_url = call.message.text
    local_file = 'document.xls'
    request.urlretrieve(remote_url, local_file)
    bot.send_document(chat_id=call.message.chat.id, document=open("./document.xls", "rb"))
    bot.send_message(chat_id=call.message.chat.id, text="دانلود با موفقیت انجام شد.")
    os.remove("./document.xls")

@bot.callback_query_handler(func=lambda call:call.data == "download_7")
def download_txt(call: CallbackQuery):
    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_document")
    remote_url = call.message.text
    local_file = 'document.txt'
    request.urlretrieve(remote_url, local_file)
    bot.send_document(chat_id=call.message.chat.id, document=open("./document.txt", "rb"))
    bot.send_message(chat_id=call.message.chat.id, text="دانلود با موفقیت انجام شد.")
    os.remove("./document.txt")

if __name__ == "__main__":
    bot.infinity_polling()