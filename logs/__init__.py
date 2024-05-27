from .utils import (
    add_named_logger
)

# request logs
request_log = add_named_logger('request')

# parser logs
parser_log = add_named_logger('parser')

# runner logs
runner_log = add_named_logger('runner')