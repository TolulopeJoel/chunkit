import os

import requests
from moviepy.editor import VideoFileClip


def split_video(file_object, num_chunks=2):
    video_file = requests.get(file_object.file.url, stream=True).raw

    video = VideoFileClip(video_file)
    duration = video.duration
    chunk_duration = duration / num_chunks
    if duration % chunk_duration != 0:
        num_chunks += 1

    chunks_folder = f"{file_object.name}_chunks"
    os.makedirs(chunks_folder, exist_ok=True)

    chunk_files = []

    for i in range(num_chunks):
        start = i * chunk_duration
        end = min((i + 1) * chunk_duration, duration)
        chunk = video.subclip(start, end)

        chunk_file_path = os.path.join(
            chunks_folder,
            f'{file_object.name}.chunk{i+1}.{file_object.type}'
        )
        chunk.write_videofile(
            chunk_file_path,
            codec="libx264",
            audio_codec="libvorbis"
        )
        chunk_files.append(chunk_file_path)

    return chunk_files
