"""Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет»,
«декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его
содержимое."""

FILENAME = 'test_file.txt'

with open(FILENAME, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        print(line)
