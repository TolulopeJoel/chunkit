import os
import shutil
import zipfile

import requests

def split_archive(object, num_chunks):
    archive_file = object.uploaded_file

    chunks_folder_name = f"{archive_file.name}_chunks"
    os.makedirs(chunks_folder_name, exist_ok=True)
    
    file_path = requests.get(archive_file.file.url, stream=True).raw

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        files_in_zip = zip_ref.namelist()
        files_per_chunk = len(files_in_zip) // num_chunks
        remaining_files = len(files_in_zip) % num_chunks

        start = 0
        end = files_per_chunk
        output_chunk_files = []

        for i in range(num_chunks):
            chunk_files = files_in_zip[start:end]
            chunk_folder = os.path.join(chunks_folder_name, f"chunk_{i+1}")
            os.makedirs(chunk_folder, exist_ok=True)

            for file in chunk_files:
                extracted_file_path = zip_ref.extract(file, path=chunk_folder)

            chunk_zip_path = os.path.join(
                chunks_folder_name,
                f'{archive_file.name}.chunk{i+1}{archive_file.type}'
            )

            shutil.make_archive(chunk_folder, archive_file.type.strip('.'), chunk_folder)
            os.rename(f"{chunk_folder}{archive_file.type}", chunk_zip_path)

            output_chunk_files.append(chunk_zip_path)

            start = end
            end += files_per_chunk if (i == num_chunks - 2) else files_per_chunk + remaining_files

        return output_chunk_files

