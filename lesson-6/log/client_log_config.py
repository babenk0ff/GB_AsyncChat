import logging
from pathlib import Path
import sys


path = Path(__file__).resolve().parent
log_file = path / 'client.log'

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s'
)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.ERROR)

file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(formatter)

client_logger = logging.getLogger('client')
client_logger.addHandler(stream_handler)
client_logger.addHandler(file_handler)
client_logger.setLevel(logging.DEBUG)
