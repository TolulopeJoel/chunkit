import os
import shutil

from environs import Env
from telegram.ext import (
    CommandHandler, ConversationHandler,
    Filters, MessageHandler, Updater
)

from archive_chunker import split_archive
from image_chunker import split_image
from pdf_chunker import split_pdf
from text_chunker import split_text
from video_chunker import split_video

env = Env()
env.read_env()

# Conversation states
GET_FILE, GET_NUM_CHUNKS, CONFIRM_CHUNKS = 1, 2, 3

file_extensions = {
    "image": (".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif", ".bmp", ".ico", ".tiff"),
    "video": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".m4v"),
    "archive": (".tar", ".gz", ".zip", ".rar", ".7z"),
    "text": (".txt", ".csv"),
    "pdf": (".pdf"),
}

file_handlers = {
    "image": split_image,
    "archive": split_archive,
    "video": split_video,
    "text": split_text,
    "pdf": split_pdf,
}


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to the File Chunker Bot!"
    )


def cancel(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Okay, the process has been cancelled."
    )

    return ConversationHandler.END


def handle_file(update, context):
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    new_file = context.bot.get_file(file_id)
    new_file.download(file_name)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="How many chunks do you want? Please enter a number."
    )

    # Save the file path in the user_data
    context.user_data["file_path"] = file_name

    # Transition to the next state
    return GET_NUM_CHUNKS


def get_num_chunks(update, context):
    num_chunks = int(update.message.text)
    context.user_data["num_chunks"] = num_chunks

    # Ask for confirmation
    response = f"You want to split the file into {num_chunks} chunks. Is that correct? (yes/no)"
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    # Transition to the next state
    return CONFIRM_CHUNKS


def confirm_chunks(update, context):
    confirmed = update.message.text.lower()

    if confirmed in ["yes", "y"]:
        file_path = context.user_data["file_path"]
        num_chunks = context.user_data["num_chunks"]

        split_function = get_split_function(file_path)
        if split_function is not None:
            chunk_files = split_function(file_path, num_chunks)
            send_chunks(update, context, chunk_files)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="File type not supported."
            )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Okay, the process has been cancelled."
        )

    # End the conversation
    return ConversationHandler.END


def get_split_function(file_path):
    file_extension = os.path.splitext(file_path)[1]

    return next(
        (
            file_handlers.get(extension_type)
            for extension_type, extensions in file_extensions.items()
            if file_extension in extensions
        ),
        None,
    )


def delete_chunks_folders():
    # Get the current working directory
    current_dir = os.getcwd()

    # Iterate over the directories in the current directory
    for directory in os.listdir(current_dir):
        if directory.endswith("_chunks") and os.path.isdir(directory):
            # Delete the directory and its contents
            shutil.rmtree(directory)
            print(f"Deleted folder: {directory}")


def send_chunks(update, context, chunk_files):
    for chunk_file in chunk_files:
        context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=open(chunk_file, "rb")
        )

    # Delete the 'chunks' folder
    delete_chunks_folders()


def main():
    # Set up the bot
    updater = Updater(
        token=env.str("BOT_TOKEN"),
        use_context=True
    )
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("cancel", cancel))

    # Set up conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.document, handle_file)],
        states={
            GET_NUM_CHUNKS: [MessageHandler(Filters.text, get_num_chunks)],
            CONFIRM_CHUNKS: [MessageHandler(Filters.text, confirm_chunks)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conversation_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
