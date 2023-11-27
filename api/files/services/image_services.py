import os

import requests
from PIL import Image


def split_image(file_object, num_chunks=2):
    """
    Split an image into multiple chunks.

    Args:
        object: The chunk object containing the uploaded file.
        num_chunks: The number of chunks to split the image into. Default is 2

    Returns:
        List[str]: A list of file paths for the generated image chunks.

    Examples:
        >>> split_image(object, num_chunks=2)
        [
            '/path/to/image_chunks/image.chunk1.png',
            '/path/to/image_chunks/image.chunk2.png'
        ]
    """
    image = Image.open(requests.get(file_object.file.url, stream=True).raw)
    image_width, image_height = image.size

    num_chunks_vertical = int(num_chunks**0.5)
    num_chunks_horizontal = num_chunks // num_chunks_vertical

    chunk_width = (
        image_width + num_chunks_horizontal - 1
    ) // num_chunks_horizontal
    chunk_height = (
        image_height + num_chunks_vertical - 1
    ) // num_chunks_vertical

    chunks_folder = f"{file_object.name}_chunks"
    os.makedirs(chunks_folder, exist_ok=True)

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
                chunks_folder,
                f"{file_object.name}.chunk{count+1}.{file_object.type}",
            )

            chunk.save(chunk_file_path)
            chunk_files.append(chunk_file_path)
            count += 1

    return chunk_files
