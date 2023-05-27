import os

def split(file_path, chunk_amount):
    with open(file_path, 'r') as text_file:
        lines = text_file.readlines()
        lines_per_file = len(lines) // chunk_amount
        remaining_lines = len(lines) % chunk_amount
        
        file_name = file_path.split('.')
        file_name = ''.join(file_name[:-1])
        
        file_parts = os.path.splitext(file_path)
        file_name = file_parts[0]
        file_extension = file_parts[1]
        
        print(os.path.splitext(file_path))
        
        start = 0
        for amount in range(chunk_amount):
            end = start + lines_per_file
            if amount < remaining_lines:
                end += 1
            
            if amount == chunk_amount - 1:
                end += remaining_lines
            
            with open(f'newpath/{file_name}.chunk{amount+1}.{file_extension}', 'w') as chunk_file:
                chunk = lines[start:end]
                chunk_file.writelines(chunk)
