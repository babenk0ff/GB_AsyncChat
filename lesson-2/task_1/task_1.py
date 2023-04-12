"""Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

- Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
данных.
- В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list.
- В этой же функции создать главный список для хранения данных отчета — например, main_data — и
поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
«Тип системы».
- Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла); Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции
реализовать получение данных через вызов функции get_data(), а также сохранение подготовленных данных в
соответствующий CSV-файл; Проверить работу программы через вызов функции write_to_csv()."""

import csv
import glob
import re

from chardet import UniversalDetector


def get_data():
    files = [file for file in glob.glob('info_*.txt')]

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [
        ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'],
    ]

    for file in files:
        # Определение кодировки файла
        detector = UniversalDetector()
        with open(file, 'rb') as f:
            for line in f:
                detector.feed(line)
            if detector.done:
                break
        detector.close()
        encoding = detector.result['encoding']

        with open(file, 'r', encoding=encoding) as f:
            file_content = f.read()
            os_prod_pattern = re.compile(r'Изготовитель системы:\s*(.*)')
            os_prod_list.append(re.findall(os_prod_pattern, file_content)[0].strip())

            os_name_pattern = re.compile(r'Название ОС:\s*(.*)')
            os_name_list.append(re.findall(os_name_pattern, file_content)[0].strip())

            os_code_pattern = re.compile(r'Код продукта:\s*(.*)')
            os_code_list.append(re.findall(os_code_pattern, file_content)[0].strip())

            os_type_pattern = re.compile(r'Тип системы:\s*(.*)')
            os_type_list.append(re.findall(os_type_pattern, file_content)[0].strip())

    for elem in list(zip(os_prod_list, os_name_list, os_code_list, os_type_list)):
        main_data.append(elem)

    return main_data


def write_to_csv(file):
    data_for_write = get_data()

    with open(file, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in data_for_write:
            writer.writerow(row)


if __name__ == '__main__':
    FILE = 'parsed_data.csv'

    write_to_csv(FILE)
