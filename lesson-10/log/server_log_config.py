import logging
from pathlib import Path
import sys
from logging.handlers import TimedRotatingFileHandler


path = Path(__file__).resolve().parent
log_file = path / 'server.log'

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s'
)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.ERROR)

file_handler = TimedRotatingFileHandler(
    log_file,
    encoding='utf-8',
    when='D',
    interval=1
)
file_handler.setFormatter(formatter)

server_logger = logging.getLogger('server')
server_logger.addHandler(stream_handler)
server_logger.addHandler(file_handler)
server_logger.setLevel(logging.DEBUG)
