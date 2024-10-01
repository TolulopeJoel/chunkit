import os
import shutil
from typing import Callable

from textblob import TextBlob

import config


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


def get_split_function(file_path: str) -> Callable:
    """Get the appropriate split function based on file extension."""
    file_extension = os.path.splitext(file_path)[1].lower()
    return next(
        (
            config.file_handlers[extension_type]
            for extension_type, extensions in config.file_extensions.items()
            if file_extension in extensions
        ),
        None,
    )


def delete_chunks_folders() -> None:
    """Delete all folders ending with '_chunks'."""
    current_dir = os.getcwd()
    for directory in os.listdir(current_dir):
        if directory.endswith("_chunks") and os.path.isdir(directory):
            shutil.rmtree(directory)
