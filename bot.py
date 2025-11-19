import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a private channel video link — I will download it 😊")


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    # Only Telegram links allowed
    if "t.me" not in url:
        await update.message.reply_text("Only Telegram links are supported.")
        return

    try:
        file = await context.bot.get_file(url)
        await file.download_to_drive("video.mp4")
        await update.message.reply_video("video.mp4")
    except:
        await update.message.reply_text("❌ I cannot access that private channel.\n\nAdd this bot to that private channel as **Admin**.")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

app.run_polling()
