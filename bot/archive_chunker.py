import os
import shutil
import zipfile
from utils import get_chunks_folder_name

def split_archive(file_path, num_chunks):
    file_name = get_chunks_folder_name(file_path)[0]
    file_extension = get_chunks_folder_name(file_path)[1]

    # create text chunks ouput folder
    chunks_folder_name = f"{file_name}_chunks"
    os.makedirs(chunks_folder_name, exist_ok=True)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
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
                extracted_file_path = zip_ref.extract(file, path=chunk_folder)

            chunk_zip_path = os.path.join(
                chunks_folder_name,
                f'{file_name}.chunk{i+1}{file_extension}'
            )
            shutil.make_archive(chunk_folder, file_extension.strip('.'), chunk_folder)
            os.rename(f"{chunk_folder}{file_extension}", chunk_zip_path)
            
            output_chunk_files.append(chunk_zip_path)

            start = end
            end += files_per_chunk

            if i == num_chunks - 2:
                end += files_per_chunk + remaining_files

        return output_chunk_files
