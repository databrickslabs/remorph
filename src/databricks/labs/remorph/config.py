import logging
from dataclasses import dataclass
from pathlib import Path

from databricks.labs.remorph.transpiler.transpile_status import ParserError
from databricks.labs.remorph.reconcile.recon_config import Table


logger = logging.getLogger(__name__)


@dataclass
class TranspileConfig:
    __file__ = "config.yml"
    __version__ = 1

    transpiler: str
    source_dialect: str | None = None
    input_source: str | None = None
    output_folder: str | None = None
    sdk_config: dict[str, str] | None = None
    skip_validation: bool = False
    catalog_name: str = "remorph"
    schema_name: str = "transpiler"
    mode: str = "current"

    @property
    def transpiler_path(self):
        return Path(self.transpiler)

    @property
    def input_path(self):
        if self.input_source is None:
            raise ValueError("Missing input source!")
        return Path(self.input_source)

    @property
    def output_path(self):
        return None if self.output_folder is None else Path(self.output_folder)

    @property
    def target_dialect(self):
        return "experimental" if self.mode == "experimental" else "databricks"


@dataclass
class TableRecon:
    __file__ = "recon_config.yml"
    __version__ = 1

    source_schema: str
    target_catalog: str
    target_schema: str
    tables: list[Table]
    source_catalog: str | None = None

    def __post_init__(self):
        self.source_schema = self.source_schema.lower()
        self.target_schema = self.target_schema.lower()
        self.target_catalog = self.target_catalog.lower()
        self.source_catalog = self.source_catalog.lower() if self.source_catalog else self.source_catalog


@dataclass
class DatabaseConfig:
    source_schema: str
    target_catalog: str
    target_schema: str
    source_catalog: str | None = None


@dataclass
class TranspilationResult:
    transpiled_sql: list[str]
    parse_error_list: list[ParserError]


@dataclass
class ValidationResult:
    validated_sql: str
    exception_msg: str | None


@dataclass
class ReconcileTablesConfig:
    filter_type: str  # all/include/exclude
    tables_list: list[str]  # [*, table1, table2]


@dataclass
class ReconcileMetadataConfig:
    catalog: str = "remorph"
    schema: str = "reconcile"
    volume: str = "reconcile_volume"


@dataclass
class ReconcileConfig:
    __file__ = "reconcile.yml"
    __version__ = 1

    data_source: str
    report_type: str
    secret_scope: str
    database_config: DatabaseConfig
    metadata_config: ReconcileMetadataConfig
    job_id: str | None = None
    tables: ReconcileTablesConfig | None = None


@dataclass
class RemorphConfigs:
    transpile: TranspileConfig | None = None
    reconcile: ReconcileConfig | None = None
