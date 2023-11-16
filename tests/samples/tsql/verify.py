import functools
import logging

from pathlib import Path

from databricks.labs.remorph.framework.entrypoint import run_main, get_logger
from databricks.labs.remorph.framework.parallel import Threads
from databricks.labs.remorph.parsers.tsql import parse_tsql, parse_tsql_dummy

logger = get_logger(__file__)
databricks_logger = logging.getLogger('databricks')
databricks_logger.setLevel('DEBUG')
databricks_logger.addHandler(logging.FileHandler('verify.log'))


def main():
    tasks = []
    __folder__ = Path(__file__).parent
    for sample in sorted(__folder__.glob('**/*.sql')):
        tasks.append(functools.partial(parse_tsql_dummy, sample))
    res, errors = Threads.gather('Parsing Transact-SQL samples', tasks, process_pool=True)
    logger.warning(f'success: {len(res)}, errors={len(errors)}')


if __name__ == '__main__':
    run_main(main)
