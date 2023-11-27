import os

import requests
from PyPDF2 import PdfReader, PdfWriter


def split_pdf(file_object, num_chunks=2):
    pdf_file = requests.get(file_object.file.url, stream=True).raw

    chunks_folder = f"{file_object.name}_chunks"
    os.makedirs(chunks_folder, exist_ok=True)

    with open(pdf_file, 'rb') as file:
        pdf = PdfReader(file)

        total_pages = len(pdf.pages)
        pages_per_chunk = total_pages // num_chunks
        remaining_pages = total_pages % num_chunks

        chunk_files = []
        start, end = 0, pages_per_chunk

        for i in range(num_chunks):
            chunk_pdf = PdfWriter()

            # Adjust 'end' if it exceeds total pages
            end = min(end, total_pages)
            for page_num in range(start, end):
                page = pdf.pages[page_num]
                chunk_pdf.add_page(page)

            chunk_file_path = os.path.join(
                chunks_folder,
                f"{file_object.name}.chunk{i+1}.{file_object.type}"
            )
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_pdf.write(chunk_file)

            chunk_files.append(chunk_file_path)

            start = end
            # if pages can't be shared equally between chunks,
            # put the remaining pages in the last chunk file.
            end += pages_per_chunk + remaining_pages if i == num_chunks - 2 else pages_per_chunk

        return chunk_files
