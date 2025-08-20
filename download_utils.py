import requests
from pathlib import Path
from file_utils import get_file_extension


def download_images(image_urls, folder, filename_prefix):
    """Скачивает изображение по URL и сохраняет в указанную папку

    Args:
        image_urls: Ссылка на изображение
        folder: Папка для сохранения (объект Path или строка)
        filename_prefix: Имя файла
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for index, url in enumerate(image_urls, start=1):
        response = requests.get(url)
        response.raise_for_status()
        ext = get_file_extension(url) or '.png'
        filename = f'{filename_prefix}{ext}'
        filepath = folder / filename

        with open(filepath, 'wb') as file:
            file.write(response.content)
