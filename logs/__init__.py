from .utils import (
    add_named_logger
)

# request logs
request_log = add_named_logger('request')

# parser logs
parser_log = add_named_logger('parser')