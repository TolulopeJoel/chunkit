import os
from pathlib import Path

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from config import CONFIRM_CHUNKS, GET_NUM_CHUNKS
from logger import logger
from utils import delete_chunks_folders, get_split_function, interpret_response


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the uploaded file and ask for the number of chunks."""
    message = update.message
    file, file_name = None, None

    # Create a folder for storing downloaded files
    downloads_folder = Path("downloads")
    downloads_folder.mkdir(exist_ok=True)

    if message.document:
        file = await message.document.get_file()
        file_name = message.document.file_name
    elif message.photo:
        file = await message.photo[-1].get_file()
        file_name = f"photo_{message.photo[-1].file_id}.jpg"
    elif message.video:
        file = await message.video.get_file()
        file_name = f"video_{message.video.file_id}.mp4"
    else:
        await message.reply_text(
            "Sorry, this file type is not supported. Please try uploading a document, photo, or video file."
        )
        return ConversationHandler.END

    # Download the file to the downloads_folder
    file_path = downloads_folder / file_name
    await file.download_to_drive(file_path)

    # Check if file type is supported
    if not get_split_function(file_path):
        await message.reply_text(
            "Sorry, this file type is not supported for splitting. Please try a different file.\nSend message to dotolulope2@gmail.com if it is life threatening."
        )
        os.remove(file_path)
        return ConversationHandler.END

    context.user_data["file_path"] = file_path

    await message.reply_text(
        "How many chunks do you want? Please enter a number or choose from the options below.",
        reply_markup=ReplyKeyboardMarkup(
            [['2', '3', '4', '5']],
            one_time_keyboard=True
        )
    )

    return GET_NUM_CHUNKS


async def get_num_chunks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Parse the number of chunks and ask for confirmation."""
    try:
        num_chunks = int(update.message.text)
        if num_chunks <= 0:
            raise ValueError("Number of chunks must be greater than 0")
        if num_chunks == 1:
            await update.message.reply_text(
                "Splitting file into a single chunk might return the file with lower size but same quality. Do you want that?",
                reply_markup=ReplyKeyboardMarkup(
                    [['Yes', 'No']], one_time_keyboard=True
                ),
            )
            context.user_data["num_chunks"] = num_chunks
            return CONFIRM_CHUNKS

    except ValueError:
        await update.message.reply_text("Please enter a valid number greater than 0")
        return GET_NUM_CHUNKS

    context.user_data["num_chunks"] = num_chunks

    await update.message.reply_text(
        f"You want to split the file into {num_chunks} chunks. Is that correct?",
        reply_markup=ReplyKeyboardMarkup(
            [['Yes', 'No']], one_time_keyboard=True
        )
    )

    return CONFIRM_CHUNKS


async def confirm_chunks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Confirm the number of chunks and process the file."""
    response = update.message.text

    confirmation = interpret_response(response)

    if confirmation is None:
        await update.message.reply_text(
            "I'm not quite sure what you mean. Could you please clarify with a simple 'yes' or 'no'?",
            reply_markup=ReplyKeyboardMarkup(
                [['Yes', 'No']], one_time_keyboard=True)
        )
        return CONFIRM_CHUNKS

    if confirmation:
        await update.message.reply_text("Great! I'll start processing your file.")
    else:
        await update.message.reply_text(
            "Operation cancelled. Send me a new file when you're ready.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    file_path = context.user_data["file_path"]
    num_chunks = context.user_data["num_chunks"]

    split_function = get_split_function(file_path)
    if split_function is None:
        await update.message.reply_text("File type not supported.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    await update.message.reply_text("Processing your file. This may take a moment...", reply_markup=ReplyKeyboardRemove())

    try:
        chunk_files = split_function(file_path, num_chunks)
        await send_chunks(update, context, chunk_files)
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        await update.message.reply_text(f"An error occurred while processing your file: {str(e)}")
    finally:
        os.remove(file_path)

    return ConversationHandler.END


async def send_chunks(update: Update, context: ContextTypes.DEFAULT_TYPE, chunk_files: list[str]) -> None:
    """Send the chunked files to the user."""
    for chunk_file in chunk_files:
        with open(chunk_file, "rb") as file:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=file)

    await update.message.reply_text("All chunks have been sent. Is there anything else I can help you with?")

    delete_chunks_folders()
