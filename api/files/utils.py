from datetime import datetime
from typing import Any

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


def get_folder_path(root_path):
    """
    Generate a folder path for cloudinary file based
    on the current date and week number.
    """
    now = datetime.now()
    day_of_month = datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1

    return f'media/{root_path}/{now.year}/{now.month}/{week_number}'


def success_response(data: Any, status_code: int = HTTP_200_OK) -> Response:
    """Generate a success response with the provided data and status code."""
    return Response({'status': 'success','data': data}, status=status_code)


def error_response(message: str, status_code: int = HTTP_400_BAD_REQUEST, errors: Any = []) -> Response:
    """Generate an error response with the provided message, errors, and status code."""
    error_data = {'status': 'error', 'errors': errors, 'message': message}
    return Response(error_data, status=status_code)
