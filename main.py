from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
import logging

logging.basicConfig(
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    butten = [[KeyboardButton(
        "/Tools")], [KeyboardButton("/Downloads")], [KeyboardButton("/help")]]
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=(f'خوش آمدید کاربر{update.effective_user.full_name}'), reply_markup=ReplyKeyboardMarkup(butten))
    await update.message.reply_text("به دنبال جه ابزاری میگردی؟")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("برای کمک به این ایدی پیام بدهید @ehsanfoudieprogrammer")


async def Tools(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
        ابزار ها
        /stackoverflow
        /Bootstrap
        /Django
        /SQL
        /docker
        /javaScript
        /jquery
        """
    )
    buttons = [[InlineKeyboardButton("ChatGpt", url="https://chat.openai.com/")], [
        InlineKeyboardButton("Number land", url="https://numberland.ir/")]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(f'{update.effective_user.full_name}'), reply_markup=InlineKeyboardMarkup(buttons))


async def stackoverflow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("stackoverflow: https://stackoverflow.com/")


async def Bootstrap2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("document_bootstrap: https://getbootstrap.com/docs/5.3/getting-started/introduction/")


async def django(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("document_Django: https://www.djangoproject.com/")


async def sql(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("document_SQL: https://www.mysql.com/")


async def docker2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("document_Docker: https://docs.docker.com/")


async def javaScript(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("document_javascript: https://javascript.info/")


async def jquery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("jquery: http://jquery.com/")

# the is have Downloads
async def Downloads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
        دانلودی ها
        /linux
        /python 
        /Bootstrap
        /vscode
        /Docker
        """
    )
    
async def linux(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("linux: https://ubuntu.com/download/desktop")


async def python(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("python: https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe")


async def bootstrap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bootstrap: https://github.com/twbs/bootstrap/releases/download/v5.3.0-alpha1/bootstrap-5.3.0-alpha1-dist.zip")


async def vscode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("vscode: https://code.visualstudio.com/Download")


async def docker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Docker: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe")


TOKEN = "5928108585:AAEDRlQGgmupa7x2QDtLtN9aU3EDbG66mpo"
app = ApplicationBuilder().token(token=TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
# the Tools
app.add_handler(CommandHandler("Tools", Tools))
app.add_handler(CommandHandler("stackoverflow", stackoverflow))
app.add_handler(CommandHandler("Bootstrap", Bootstrap2))
app.add_handler(CommandHandler("django", django))
app.add_handler(CommandHandler("sql", sql))
app.add_handler(CommandHandler("docker2", docker2))
app.add_handler(CommandHandler("javaScript", javaScript))
app.add_handler(CommandHandler("jquery", jquery))
# the Downloads
app.add_handler(CommandHandler("Downloads", Downloads))
app.add_handler(CommandHandler("linux", linux))
app.add_handler(CommandHandler("python", python))
app.add_handler(CommandHandler("bootstrap", bootstrap))
app.add_handler(CommandHandler("docker", docker))
app.add_handler(CommandHandler("vscode", vscode))

if __name__ == "__main__":
    app.run_polling()