import os
import requests


def split_text(file_object, num_chunks=2):
    """
    Splits a text file into multiple chunks.

    Args:
        file_object: The file object representing the text file.
        num_chunks: The number of chunks to split the text file into.

    Returns:
        list: A list of file paths representing the output chunk files.

    Raises:
        None
    """

    response = requests.get(file_object.file.url, stream=True)
    text_content = response.content.decode('utf-8')

    file_lines = text_content.splitlines()
    num_file_lines = len(file_lines)
    lines_per_chunk = num_file_lines // num_chunks
    remaining_lines = num_file_lines % num_chunks

    start_line = 0
    end_line = lines_per_chunk
    chunk_files = []

    chunks_folder = f"{file_object.name}_chunks"
    os.makedirs(chunks_folder, exist_ok=True)

    for i in range(num_chunks):
        chunk_file_path = os.path.join(
            chunks_folder,
            f'{file_object.name}.chunk{i+1}.{file_object.type}'
        )
        with open(chunk_file_path, "w") as chunk_file:
            chunk = file_lines[start_line:end_line]
            chunk_file.write("\n".join(chunk))
        chunk_files.append(chunk_file_path)

        start_line = end_line
        end_line += lines_per_chunk

        # if lines can't be shared equal length between chunks,
        # put the remaining lines in the last chunk file.
        if i == num_chunks - 2:
            end_line += lines_per_chunk + remaining_lines

    return chunk_files
