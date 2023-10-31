from datetime import datetime


def get_folder_path(root_path):
    """
    Generate a folder path for cloudinary file based
    on the current date and week number.
    """

    # Current date and time
    now = datetime.now()

    # Calculate the week number of current month
    day_of_month = datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1

    return f'media/{root_path}/{now.year}/{now.month}/{week_number}'
