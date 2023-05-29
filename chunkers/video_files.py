import os

from moviepy.editor import VideoFileClip


def split(file_path, num_chunks=2):
    video = VideoFileClip(file_path)
    duration = video.duration
    chunk_duration = duration / num_chunks
    if duration % chunk_duration != 0:
        num_chunks += 1

    # file names and extension
    file_basename = os.path.basename(file_path)
    file_pathname = os.path.splitext(file_basename)
    file_name, file_extension = file_pathname

    # create text chunks ouput folder
    chunks_folder_name = f"{file_name}_chunks"
    os.makedirs(chunks_folder_name, exist_ok=True)

    for i in range(num_chunks):
        start = i * chunk_duration
        end = min((i + 1) * chunk_duration, duration)
        chunk = video.subclip(start, end)

        chunk_file_path = os.path.join(
            chunks_folder_name,
            f'{file_name}.chunk{i+1}{file_extension}'
        )
        chunk.write_videofile(
            chunk_file_path, codec="libx264", audio_codec="libvorbis")

        print(f"Chunk {i+1} created: {chunk_file_path}")
