"""Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
скрипт, автоматизирующий его заполнение данными. Для этого: Создать функцию write_order_to_json(), в которую
передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция
должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в
4 пробельных символа; Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений
каждого параметра."""

import json
import os.path


def write_order_to_json(item, quantity, price, buyer, date):
    file = 'orders.json'

    new_order = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date,
    }

    if os.path.exists(file) and os.stat(file).st_size != 0:
        with open(file, 'r') as f:
            file_content = json.load(f)
    else:
        file_content = {'orders': []}

    with open(file, 'w+') as f:
        file_content['orders'].append(new_order)
        json.dump(file_content, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    write_order_to_json(item="сканер",  quantity=2, price=10000, buyer='Ivanov I.I.', date="11.01.2018")
    write_order_to_json(item="компьютер",  quantity=5, price=40000, buyer='Сидоров С.С.', date="2.05.2019")
