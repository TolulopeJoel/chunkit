import os

from utils import get_chunks_folder_name


def split_text(file_path, num_chunks=2):
    file_name = get_chunks_folder_name(file_path)[0]
    file_extension = get_chunks_folder_name(file_path)[1]

    # create text chunks ouput folder
    chunks_folder_name = f"{file_name}_chunks"
    os.makedirs(chunks_folder_name, exist_ok=True)

    with open(file_path, "r") as text_file:
        file_lines = text_file.readlines()
        num_file_lines = len(file_lines)
        lines_per_chunk = num_file_lines // num_chunks
        remaining_lines = num_file_lines % num_chunks

    start_line = 0
    end_line = lines_per_chunk
    chunk_files = []

    for i in range(num_chunks):
        chunk_file_path = os.path.join(
            chunks_folder_name,
            f'{file_name}.chunk{i+1}{file_extension}'
        )
        with open(f"{chunk_file_path}", "w") as chunk_file:
            chunk = file_lines[start_line:end_line]
            chunk_file.writelines(chunk)
        chunk_files.append(chunk_file_path)

        start_line = end_line
        end_line += lines_per_chunk

        # if lines can't be shared equal length between chunks,
        # put the remaining lines in the last chunk file.
        if i == num_chunks - 2:
            end_line += lines_per_chunk + remaining_lines

    return chunk_files
