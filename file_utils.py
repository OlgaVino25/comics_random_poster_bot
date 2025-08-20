from urllib.parse import urlsplit, unquote
from os.path import splitext, split


def get_file_extension(url: str) -> str:
    """Извлекает расширение файла из URL"""
    parsed_url = urlsplit(url)
    path = unquote(parsed_url.path)
    filename = split(path)[1]
    _, ext = splitext(filename)
    return ext.lower()
