import os

from PIL import Image

from utils import get_chunks_folder_name


def split_image(file_path, num_chunks):
    file_name = get_chunks_folder_name(file_path)[0]
    file_extension = get_chunks_folder_name(file_path)[1]

    image = Image.open(file_path)
    image_width, image_height = image.size

    num_chunks_horizontal = int(num_chunks ** 0.5)
    num_chunks_vertical = num_chunks // num_chunks_horizontal

    chunk_width = (image_width + num_chunks_horizontal - 1) // num_chunks_horizontal
    chunk_height = (image_height + num_chunks_vertical - 1) // num_chunks_vertical

    chunks_folder_name = file_name + '_chunks'
    os.makedirs(chunks_folder_name, exist_ok=True)

    count = 0
    chunk_files = []

    for y_pixels in range(num_chunks_vertical):
        for x_pixels in range(num_chunks_horizontal):
            left = x_pixels * chunk_width
            upper = y_pixels * chunk_height
            right = min((x_pixels + 1) * chunk_width, image_width)
            lower = min((y_pixels + 1) * chunk_height, image_height)

            chunk = image.crop((left, upper, right, lower))
            chunk_file_path = os.path.join(
                chunks_folder_name,
                f'{file_name}.chunk{count+1}{file_extension}'
            )
            chunk.save(chunk_file_path)
            chunk_files.append(chunk_file_path)
            count += 1

    return chunk_files
