class APIError(Exception):
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

    def __str__(self):
        return 'Произошла ошибка, {}: {}'.format(self.code, self.detail)
