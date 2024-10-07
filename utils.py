import os
import shutil
from pathlib import Path

from textblob import TextBlob


def get_chunks_folder_name(file_path):
    file_basename = os.path.basename(file_path)
    file_pathname = os.path.splitext(file_basename)
    file_name, file_extension = file_pathname

    return file_name, file_extension


def interpret_response(response: str) -> bool:
    """Interpret user response using sentiment analysis."""
    response = response.lower()

    # explicit word lists
    positive_keywords = {
        'yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'fine', 'good', 'great', 'absolutely',
        'certainly', 'indeed', 'affirmative', 'roger', 'aye', 'yea', 'why not', 'go ahead', 'do it'
    }
    negative_keywords = {
        'no', 'nope', 'nah', 'not', 'negative', 'never', 'cancel', 'stop', 'don\'t', 'wait'
    }

    # Check for exact matches first
    if any(keyword in response for keyword in positive_keywords):
        return True
    if any(keyword in response for keyword in negative_keywords):
        return False

    blob = TextBlob(response)
    sentiment = blob.sentiment.polarity

    if sentiment > 0.1:
        return True
    elif sentiment < -0.1:
        return False

    # If sentiment is neutral, return None to indicate unclear response
    return None


def delete_chunks_folders() -> None:
    """Delete all folders ending with '_chunks'."""
    current_dir = os.getcwd()
    for directory in os.listdir(current_dir):
        if directory.endswith("_chunks") and os.path.isdir(directory):
            shutil.rmtree(directory)


async def get_file_info(message):
    # Create a folder for storing downloaded files
    downloads_folder = Path("downloads")
    downloads_folder.mkdir(exist_ok=True)

    if message.document:
        return (
            await message.document.get_file(),
            downloads_folder / message.document.file_name,
            message.document.file_size,
            Path(message.document.file_name).suffix.strip('.').lower()
        )
    elif message.photo:
        photo = message.photo[-1]
        return (
            await photo.get_file(),
            downloads_folder / f"photo_{photo.file_id}.jpeg",
            photo.file_size,
            'jpeg'
        )
    elif message.video:
        return (
            await message.video.get_file(),
            downloads_folder / f"video_{message.video.file_id}.mp4",
            message.video.file_size,
            'pdf'
        )
    return None


def format_size(size):
    return f"{size} MB"
