from abc import ABC, abstractmethod
from typing import List, Any, Iterable

from databricks.labs.remorph.discovery.table import TableDefinition


class TableDefinitionService(ABC):
    @abstractmethod
    def _get_table_definition(self, catalog_name: str, connection: Any) -> Iterable[TableDefinition]:
        pass

    @abstractmethod
    def _get_table_definition_query(self, catalog_name: str) -> str:
        pass
