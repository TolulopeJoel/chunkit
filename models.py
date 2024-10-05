from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    total_size: int = 0
    created_at: datetime
    total_attempts: int = 0
    files_uploaded: int = 0
    largest_file_size: int = 0
    successful_processes: int = 0
    slowest_process_time: float = 0
    activity_hours: set[int] = set()
    file_type_counts: dict[str, int] = {}
    smallest_file_size: int = float('inf')
    fastest_process_time: float = float('inf')
