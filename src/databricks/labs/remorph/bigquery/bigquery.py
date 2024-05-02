import logging
from typing import ClassVar

from sqlglot.dialects import bigquery as org

logger = logging.getLogger(__name__)


class BigQuery(org.BigQuery):
    # Instantiate BigQuery Dialect
    bigquery = org.BigQuery()

    class Parser(org.BigQuery.Parser):
        FUNCTIONS: ClassVar[dict] = {
            **org.BigQuery.Parser.FUNCTIONS,
            # TODO:  Add BigQuery specific functions implementation here
        }
