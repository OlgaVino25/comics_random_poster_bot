import os
import random
import requests
import telebot
from dotenv import load_dotenv


def get_latest_comic_num():
    """Получает номер последнего комикса"""
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()['num']


def get_comic_data(comic_id):
    """Получает данные комикса по его номеру"""
    url = f'https://xkcd.com/{comic_id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_image(url, path):
    """Скачивает и сохраняет изображение по указанному пути"""
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def get_random_comic(folder='comics_images'):
    """Основная функция для получения случайного комикса"""
    latest_num = get_latest_comic_num()
    comic_id = random.randint(1, latest_num)

    comic_data = get_comic_data(comic_id)
    image_url = comic_data['img']
    alt_text = comic_data['alt']

    file_extension = os.path.splitext(image_url)[1] or '.png'
    filename = f"comic_{comic_id}{file_extension}"
    filepath = os.path.join(os.getcwd(), filename)

    download_image(image_url, filepath)
    return filepath, alt_text


def send_to_telegram(image_path, caption, token, chat_id):
    """Отправляет изображение в Telegram"""
    bot = telebot.TeleBot(token=token)
    with open(image_path, 'rb') as photo_file:
        bot.send_photo(chat_id=chat_id, photo=photo_file, caption=caption)


def main():
    load_dotenv()
    token = os.getenv('COMICS_PYTHON_BOT_TG_TOKEN')
    chat_id = os.getenv('COMICS_PYTHON_BOT_GROUP_CHAT_ID')

    if not token or not chat_id:
        print("Ошибка: Не указаны токен или chat_id в переменных окружения")
        return

    image_path = None

    try:
        print("Скачиваю случайный комикс...")
        image_path, caption = get_random_comic()

        print("Публикую комикс в Telegram...")
        send_to_telegram(image_path, caption, token, chat_id)

        print("Готово! Комикс опубликован.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if image_path and os.path.exists(image_path):
            print("Удаляю временный файл...")
            os.remove(image_path)


if __name__ == '__main__':
    main()
