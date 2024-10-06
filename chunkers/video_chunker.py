import os
from pathlib import PosixPath

from moviepy.editor import VideoFileClip

from utils import get_chunks_folder_name


def split_video(file_path, num_chunks=2):
    file_name = get_chunks_folder_name(file_path)[0]
    file_extension = get_chunks_folder_name(file_path)[1]

    if isinstance(file_path, PosixPath):
        file_path = str(file_path)

    video = VideoFileClip(file_path)
    duration = video.duration
    chunk_duration = duration / num_chunks
    if duration % chunk_duration != 0:
        num_chunks += 1

    # create text chunks ouput folder
    chunks_folder_name = f"{file_name}_chunks"
    os.makedirs(chunks_folder_name, exist_ok=True)

    chunk_files = []

    for i in range(num_chunks):
        start = i * chunk_duration
        end = min((i + 1) * chunk_duration, duration)
        chunk = video.subclip(start, end)

        chunk_file_path = os.path.join(
            chunks_folder_name,
            f'{file_name}.chunk{i+1}{file_extension}'
        )
        chunk.write_videofile(
            chunk_file_path,
            codec="libx264",
            audio_codec="libvorbis"
        )
        chunk_files.append(chunk_file_path)

    return chunk_files
