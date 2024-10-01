from telegram import BotCommand, ReplyKeyboardRemove, Update
from telegram.ext import Application, ContextTypes, ConversationHandler


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Welcome to the File Chunker Bot, {user.mention_html()}! "
        "Please send me a file to split into chunks."
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
