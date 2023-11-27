import os
import shutil
import zipfile

import requests

def split_archive(file_object, num_chunks=2):
    chunks_folder_name = f"{file_object.name}_chunks"
    os.makedirs(chunks_folder_name, exist_ok=True)
    archive_file = requests.get(file_object.file.url, stream=True).raw

    with zipfile.ZipFile(archive_file, 'r') as zip_ref:
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


