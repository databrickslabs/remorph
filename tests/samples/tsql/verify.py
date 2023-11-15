import functools
import logging

from pathlib import Path

from databricks.labs.remorph.framework.entrypoint import run_main, get_logger
from databricks.labs.remorph.framework.parallel import Threads
from databricks.labs.remorph.parsers.tsql import parse_tsql, parse_tsql_dummy

logger = get_logger(__file__)
logging.getLogger('databricks').setLevel('DEBUG')


def main():
    tasks = []
    __folder__ = Path(__file__).parent
    for sample in sorted(__folder__.glob('**/*.sql')):
        tasks.append(functools.partial(parse_tsql_dummy, sample))
    res, errors = Threads.gather('Parsing Transact-SQL samples', tasks)
    logger.warning(f'success: {len(res)}, errors={len(errors)}')


if __name__ == '__main__':
    run_main(main)
