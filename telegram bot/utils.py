import os


def get_chunks_folder_name(file_path):
    file_basename = os.path.basename(file_path)
    file_pathname = os.path.splitext(file_basename)
    file_name, file_extension = file_pathname
    
    return file_name, file_extension
