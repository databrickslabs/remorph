import logging
from typing import ClassVar

from sqlglot.dialects.bigquery import BigQuery

logger = logging.getLogger(__name__)


# pylint: disable=function-redefined
class BigQuery(BigQuery):
    # Instantiate BigQuery Dialect
    bigquery = BigQuery()

    class Parser(BigQuery.Parser):
        FUNCTIONS: ClassVar[dict] = {
            **BigQuery.Parser.FUNCTIONS,
            # TODO:  Add BigQuery specific functions implementation here
        }
