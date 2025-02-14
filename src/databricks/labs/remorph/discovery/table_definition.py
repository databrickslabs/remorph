from abc import ABC, abstractmethod

from databricks.labs.remorph.discovery.table import TableDefinition


class TableDefinitionService(ABC):
    @abstractmethod
    def get_table_definition(self, catalog_name: str) -> [TableDefinition]:
        pass

    @abstractmethod
    def get_table_definition_query(self, catalog_name: str) -> str:
        pass
