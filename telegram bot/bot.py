
from environs import Env
from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from commands import cancel_command, help_command, set_commands, start_command
from handlers import confirm_chunks, get_num_chunks, handle_file
from utils import CONFIRM_CHUNKS, GET_NUM_CHUNKS

env = Env()
env.read_env()


def main() -> None:
    """Set up and run the bot."""
    application = Application.builder().token(env.str("BOT_TOKEN")).build()

    # Set up commands for the command menu
    application.job_queue.run_once(set_commands, when=1)

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Document.ALL, handle_file)],
        states={
            GET_NUM_CHUNKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_num_chunks)],
            CONFIRM_CHUNKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_chunks)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
