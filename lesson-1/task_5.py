"""Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтового в строковый тип на
кириллице."""

import subprocess
import chardet


args = [
    ('ping', '-c 5', 'yandex.ru'),
    ('ping', '-c 5', 'youtube.com'),
]

for arg in args:
    subproc_ping = subprocess.Popen(arg, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        char_enc = chardet.detect(line)
        print(line.decode(char_enc['encoding']).strip())
