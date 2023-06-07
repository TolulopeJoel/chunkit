from PyPDF2 import PdfReader, PdfWriter
import os

def split(file_path, num_chunks):
    # file names and extension
    file_basename = os.path.basename(file_path)
    file_pathname = os.path.splitext(file_basename)
    file_name, file_extension = file_pathname

    # create PDF chunks output folder
    chunks_folder_name = f"{file_name}_chunks"
    os.makedirs(chunks_folder_name, exist_ok=True)

    with open(file_path, 'rb') as file:
        pdf = PdfReader(file)

        total_pages = len(pdf.pages)
        pages_per_chunk = total_pages // num_chunks
        remaining_pages = total_pages % num_chunks

        start = 0
        end = pages_per_chunk

        for i in range(num_chunks):
            chunk_pdf = PdfWriter()

            # Adjust 'end' if it exceeds total pages
            if end > total_pages:
                end = total_pages

            for page_num in range(start, end):
                page = pdf.pages[page_num]
                chunk_pdf.add_page(page)

            chunk_file_path = os.path.join(
                chunks_folder_name,
                f"{file_name}.chunk{i+1}{file_extension}"
            )
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_pdf.write(chunk_file)
                
            start = end
            end += pages_per_chunk

            # if pages can't be shared equally between chunks,
            # put the remaining pages in the last chunk file.
            if i == num_chunks - 2:
                end += pages_per_chunk + remaining_pages
        
            print(f'Chunk {i+1} created: {chunk_file_path}')
