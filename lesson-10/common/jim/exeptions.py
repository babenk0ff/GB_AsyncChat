class InvalidJIM(Exception):
    def __str__(self):
        return 'Получена неверная JSON-строка'
