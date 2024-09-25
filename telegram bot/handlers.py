import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from config import CONFIRM_CHUNKS, GET_NUM_CHUNKS
from logger import logger
from utils import delete_chunks_folders, get_split_function, interpret_response


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the uploaded file and ask for the number of chunks."""
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    await file.download_to_drive(file_name)

    # Check if file type is supported
    if not get_split_function(file_name):
        await update.message.reply_text(
            "Sorry, this file type is not supported. Please try a different file."
        )
        os.remove(file_name)
        return ConversationHandler.END

    context.user_data["file_path"] = file_name

    reply_keyboard = [['2', '3', '4', '5']]
    await update.message.reply_text(
        "How many chunks do you want? Please enter a number or choose from the options below.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )

    return GET_NUM_CHUNKS


async def get_num_chunks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Parse the number of chunks and ask for confirmation."""
    try:
        num_chunks = int(update.message.text)
        if num_chunks <= 0:
            raise ValueError("Number of chunks must be greater than 0")
        if num_chunks == 1:
            reply_keyboard = [['Yes', 'No']]
            await update.message.reply_text(
                "Splitting file into a single chunk might return the file with lower size but same quality. Do you want that?",
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True
                ),
            )
            context.user_data["num_chunks"] = num_chunks
            return CONFIRM_CHUNKS

    except ValueError:
        await update.message.reply_text("Please enter a valid number greater than 0")
        return GET_NUM_CHUNKS

    context.user_data["num_chunks"] = num_chunks

    reply_keyboard = [['Yes', 'No']]
    await update.message.reply_text(
        f"You want to split the file into {num_chunks} chunks. Is that correct?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
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

    return ConversationHandler.END


async def send_chunks(update: Update, context: ContextTypes.DEFAULT_TYPE, chunk_files: list[str]) -> None:
    """Send the chunked files to the user."""
    for chunk_file in chunk_files:
        with open(chunk_file, "rb") as file:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=file)

    await update.message.reply_text("All chunks have been sent. Is there anything else I can help you with?")

    delete_chunks_folders()
