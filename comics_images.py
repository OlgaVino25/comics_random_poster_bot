import argparse
import requests
import random
from download_utils import download_images


def fetch_comics_images(comic_id=None, folder='images', filename_prefix='comics'):
    """
    Скачивает указанный комикс с xkcd или случайный комикс, если comic_id не указан.

    Args:
        comic_id (int, optional): Номер комикса. Если None - случайный комикс, 0 - последний комикс.
        folder (str, optional): Папка для сохранения изображения.
        filename_prefix (str, optional): Префикс для имени файла.

    Raises:
        requests.exceptions.RequestException: При ошибке запроса к API xkcd.
    """
    latest_response = requests.get('https://xkcd.com/info.0.json')
    latest_response.raise_for_status()
    latest_comic = latest_response.json()
    max_num = latest_comic['num']

    if comic_id is None:
        comic_id = random.randint(1, max_num)
        print(f"Выбран случайный комикс с номером: {comic_id}")

    if comic_id == 0:
        url = 'https://xkcd.com/info.0.json'
    else:
        url = f'https://xkcd.com/{comic_id}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()

    image_url = comic_data['img']
    comment = comic_data['alt']
    num = comic_data['num']
    print(f'Найден комикс: {comic_data["title"]}')
    print(f'Номер: {num}')
    print(f'Комментарий: {comment}')
    print('Скачиваю изображение...')

    download_images([image_url], folder, f'{filename_prefix}_{num}')
    print('Готово!')

    return {
        'title': comic_data['title'],
        'num': num,
        'alt': comment,
        'img_url': image_url
    }


def parse_arguments():
    """Парсит аргументы командной строки и загружает переменные окружения.

    Returns:
        Namespace: Объект с аргументами командной строки
    """
    parser = argparse.ArgumentParser(description='Скачивание комикса xkcd')
    parser.add_argument('--comic_id', type=int, default=None, help='Номер комикса (0 для последнего, не указывайте для случайного)')
    parser.add_argument('--folder', default='comics_images', metavar='', help='Папка для сохранения')
    parser.add_argument('--filename_prefix', default='comics', metavar='', help='Имя файлов')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    fetch_comics_images(
        comic_id=args.comic_id,
        folder=args.folder,
        filename_prefix=args.filename_prefix
    )


if __name__ == '__main__':
    main()
