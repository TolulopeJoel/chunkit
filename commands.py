from telegram import BotCommand, ReplyKeyboardRemove, Update
from telegram.ext import Application, ContextTypes, ConversationHandler

from database import user_db
from utils import format_size


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


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.application.create_task
    user_id = update.effective_user.id
    user = await user_db.get_user(user_id)

    if not user:
        await update.message.reply_text(
            "No stats available yet. Start uploading files!"
        )
        return

    # Calculate stats
    file_types = user.get("file_type_counts", {})
    most_common_type = max(file_types.items(), key=lambda x: x[1])[
        0] if file_types else "None"

    stats_message = f"""
🤖 Your ChunkIt Stats 📊

🗓️ Chunking since: {user['created_at'].strftime('%B %d, %Y')}

📈 PROCESSING METRICS:
📁 Files processed: {user.get('files_uploaded', 0)}
💾 Total data: {format_size(user.get('total_size', 0))}
🏃‍♂️ Fastest process: {user.get('fastest_process_time', 0):.2f}s
🐌 Slowest process: {user.get('slowest_process_time', 0):.2f}s


📋 FILE VARIETY:
🏆 Most used file type: {most_common_type}
📚 Unique types: {len(file_types)}
🐘 Largest file: {format_size(user.get('largest_file_size', 0))}
🐜 Smallest file: {format_size(user.get('smallest_file_size', float('inf')))}
🪓 Chunks received: {user.get('chunks_sent', 0)}

⏰ TIMING PATTERNS:
📅 Current streak: {user.get('current_streak', 0)} days
🔥 Longest streak: {user.get('longest_streak', 0)} days
⏱️ Active hours: {len(user.get('activity_hours', []))} different hours
    """

# TODO:
# user_rank, total_users = await user_db.get_user_rank(user_id)
# ✅ Success rate: {(user.get('successful_processes', 0) / user.get('total_attempts', 1) * 100):.1f}%
# 📈 WORLD RANK: #{user_rank} of {total_users} users

    if achievements := user.get('achievements', []):
        stats_message += "\n🏆 ACHIEVEMENTS:\n" + "\n".join(achievements)

    await update.message.reply_text(stats_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        """
        This bot can split various types of files into smaller chunks.\nSupported file types include images, videos, archives, text files, and PDFs.\n
        To use the bot:
        1. Send a file you want to split
        2. Specify the number of chunks
        3. Confirm your choice\n
        Commands:
        🚀 /start - Start the bot
        💡 /help - Show this help message
        📊 /stats - Show the bot usage
        🚫 /cancel - Cancel the current operation"""
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
        BotCommand("stats", "Show some interesting figures"),
        BotCommand("cancel", "Cancel the current operation"),
    ]
    await application.bot.set_my_commands(commands)