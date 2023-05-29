import os


def split(file_path, num_chunks=2):
    with open(file_path, "r") as text_file:
        file_lines = text_file.readlines()
        num_file_lines = len(file_lines)
        lines_per_chunk = int(num_file_lines / num_chunks)
        remaining_lines = 0

        total_lpc = lines_per_chunk * num_chunks # total lines for all chunks
        if total_lpc < num_file_lines:
            remaining_lines = num_file_lines - total_lpc

    # file names and extension
    file_basename = os.path.basename(file_path)
    file_pathname = os.path.splitext(file_basename)
    file_name, file_extension = file_pathname

    # create text chunks ouput folder
    chunks_folder_name = f"{file_name}_chunks"
    os.makedirs(chunks_folder_name, exist_ok=True)

    start_line = 0
    end_line = lines_per_chunk

    for i in range(num_chunks):
        chunk_file_path = os.path.join(
            chunks_folder_name,
            f'{file_name}.chunk{i+1}{file_extension}'
        )
        with open(f"{chunk_file_path}", "w") as chunk_file:
            chunk = file_lines[start_line:end_line]
            chunk_file.writelines(chunk)

        start_line = end_line
        end_line += lines_per_chunk

        # if lines can't be shared equal length between chunks,
        # put the remaining lines in the last chunk file.
        if i == num_chunks - 2:
            end_line += lines_per_chunk + remaining_lines

        print(f'Chunk {i+1} created: {chunk_file_path}')
