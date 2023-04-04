"""Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в
байтовое и выполнить обратное преобразование (используя методы encode и decode)."""

words = [
    'разработка',
    'администрирование',
    'protocol',
    'standard',
]

for word in words:
    encoded = word.encode('utf-8')
    decoded = encoded.decode('utf-8')
    print(encoded, decoded)
    print()
