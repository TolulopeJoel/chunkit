from database import user_db
from telegram import BotCommand, ReplyKeyboardRemove, Update
from telegram.ext import Application, ContextTypes, ConversationHandler


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id

    existing_user = await user_db.get_user(user_id)
    if existing_user:
        await update.message.reply_html(
            rf"Welcome back, {user.first_name}! "
            "Ready to chunk some more files? Let's see those stats grow! 📈"
        )
    else:
        await user_db.create_user({
            "user_id": user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        })

        await update.message.reply_html(
            f"Hello {user.mention_html()}, it's a pleasure to have you here! 🎉\n\n"
            "I'm prepared to assist you in splitting your files into well-organized chunks."
            "Please feel free to send any file, and I will handle the rest. ✨\n\n"
            "Tip: You can check your file processing statistics at any time by using /stats."
        )




async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        """
        This bot can split various types of files into smaller chunks.\nSupported file types include images, videos, archives, text files, and PDFs.\n
        To use the bot:
        1. Send a file you want to split
        2. Specify the number of chunks
        3. Confirm your choice\n
        Commands:
        /start - Start the bot
        /help - Show this help message
        /cancel - Cancel the current operation"""
    )
    await update.message.reply_text(help_text)


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE, chunk_files: list[str]) -> int:
    await update.message.reply_text(
        "Operation cancelled. Send me a new file when you're ready.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def set_commands(application: Application) -> None:
    """Set bot commands to display in the command menu."""
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help message"),
        BotCommand("cancel", "Cancel the current operation"),
    ]
    await application.bot.set_my_commands(commands)
