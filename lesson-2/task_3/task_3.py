"""Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
YAML-формата. Для этого: Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €); Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить
возможность работы с юникодом: allow_unicode = True; Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными."""

import yaml

file = 'file.yaml'

data = {
    'list': ['item_1', 'item_2', 'item_3'],
    'integer': 123,
    'dict': {
        'inner_1': '123€',
        'inner_2': '300€',
    },
}

with open(file, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

with open(file) as f:
    print(yaml.safe_load(f) == data)
