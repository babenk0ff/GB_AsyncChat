import functools
import inspect

from .server_log_config import *
from .client_log_config import *

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        caller = inspect.stack()[1][3]
        result = func(*args, **kwargs)
        logger.debug(f'Функция {func.__name__} с аргументами '
                     f'args {args}, kwargs {kwargs} '
                     f'была вызвана из функции: {caller}')
        return result

    return wrapper
