import time

from logs import runner_log
from src.parser_service import WildberriesParser
from src.request_service import RequestManager

from src.runner import Runner


def main():
    runner = Runner(WildberriesParser(), RequestManager())
    runner.run(pages=1, workers=4)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    runner_log.info(f'Total time for data collection: {end}')
