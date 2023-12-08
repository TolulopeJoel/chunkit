import os
import shutil
import zipfile

import requests

def split_archive(file_object, num_chunks=2):
    """
    Splits an archive file into multiple chunks.

    Args:
        file_object: The file object representing the archive file.
        num_chunks: The number of chunks to split the archive into.

    Returns:
        list: A list of file paths representing the output chunk files.

    Raises:
        None
    """

    chunks_folder_name = f"{file_object.name}_chunks"
    os.makedirs(chunks_folder_name, exist_ok=True)
    archive_file = requests.get(file_object.file.url, stream=True).raw

    with zipfile.ZipFile(archive_file, 'r') as zip_ref:
        return extract_and_split_archive(
            zip_ref, num_chunks, chunks_folder_name, file_object
        )


def extract_and_split_archive(zip_ref, num_chunks, chunks_folder_name, file_object):
    """
    Extracts and splits an archive into multiple chunks.

    Args:
        zip_ref (zipfile.ZipFile): The ZipFile object representing the archive to be split.
        num_chunks (int): The number of chunks to split the archive into.
        chunks_folder_name (str): The name of the folder to store the chunks.
        file_object: The file object representing the archive file.

    Returns:
        list: A list of file paths representing the output chunk files.

    Raises:
        None
    """

    files_in_zip = zip_ref.namelist()
    files_per_chunk = len(files_in_zip) // num_chunks
    remaining_files = len(files_in_zip) % num_chunks

    output_chunk_files = []
    start = 0
    end = files_per_chunk
    for i in range(num_chunks):
        chunk_files = files_in_zip[start:end]
        chunk_folder = os.path.join(chunks_folder_name, f"chunk_{i+1}")
        os.makedirs(chunk_folder, exist_ok=True)

        for file in chunk_files:
            zip_ref.extract(file, path=chunk_folder)

        chunk_zip_path = os.path.join(
            chunks_folder_name,
            f'{file_object.name}.chunk{i+1}{file_object.type}'
        )
        shutil.make_archive(chunk_folder, file_object.type.strip('.'), chunk_folder)
        os.rename(f"{chunk_folder}{file_object.type}", chunk_zip_path)

        output_chunk_files.append(chunk_zip_path)

        start = end
        end += files_per_chunk

        if i == num_chunks - 2:
            end += files_per_chunk + remaining_files

    return output_chunk_files


