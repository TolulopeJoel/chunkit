import os

from PIL import Image


def split(file_path, num_chunks=2):
    image = Image.open(file_path)
    image_width, image_height = image.size

    num_chunks_horizontal = int(num_chunks ** 0.5)
    num_chunks_vertical = num_chunks // num_chunks_horizontal

    chunk_width = image_width // num_chunks_horizontal
    chunk_height = image_height // num_chunks_vertical

    if image_width % num_chunks_horizontal != 0:
        chunk_width += 1

    if image_height % num_chunks_vertical != 0:
        chunk_height += 1

    # file names and extension
    file_basename = os.path.basename(file_path)
    file_pathname = os.path.splitext(file_basename)
    file_name, file_extension = file_pathname

    # create image chunks ouput folder
    chunks_folder_name = f'{file_name}_chunks'
    os.makedirs(chunks_folder_name, exist_ok=True)

    count = 0
    for y_pixels in range(num_chunks_vertical):
        for x_pixels in range(num_chunks_horizontal):
            left = x_pixels * chunk_width
            upper = y_pixels * chunk_height
            right = min((x_pixels + 1) * chunk_width, image_width)
            lower = min((y_pixels + 1) * chunk_height, image_height)

            # export and save chunk image files to chunk output folder
            chunk = image.crop((left, upper, right, lower))
            chunk_file_path = os.path.join(
                chunks_folder_name,
                f'{file_name}.chunk{count+1}{file_extension}'
            )
            chunk.save(chunk_file_path)
            count += 1

            print(f'Chunk {count} created: {chunk_file_path}')
