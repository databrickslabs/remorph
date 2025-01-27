import json
from dataclasses import asdict

from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.reconcile.recon_config import Table, Aggregate, JdbcReaderOptions, ColumnMapping, \
    Transformation, ColumnThresholds, Filters, TableThresholds


def generate_json_file(table_recon: TableRecon, file_name: str):
    def serialize(obj):
        """Helper function to handle optional complex objects"""
        if isinstance(obj, (Aggregate, JdbcReaderOptions, ColumnMapping, Transformation, ColumnThresholds, Filters, TableThresholds)):
            return asdict(obj)  # Serialize dataclass objects
        raise TypeError(f"Type {type(obj)} not serializable")

    table_recon_dict = asdict(table_recon)
    json_data = json.dumps(table_recon_dict, default=serialize, indent=2)

    with open(file_name, 'w') as json_file:
        json_file.write(json_data)

table1 = Table(
    source_name="<SOURCE_NAME_1>",
    target_name="<TARGET_NAME_1>",
    join_columns=["<COLUMN_NAME_1>", "<COLUMN_NAME_2>"]
)
table2 = Table(
    source_name="<SOURCE_NAME_2>",
    target_name="<TARGET_NAME_2>",
    join_columns=["<COLUMN_NAME_3>", "<COLUMN_NAME_4>"]
)
table_recon = TableRecon(
    source_schema="<SOURCE_SCHEMA>",
    target_catalog="<TARGET_CATALOG>",
    target_schema="<TARGET_SCHEMA>",
    tables=[table1, table2],
    source_catalog="<SOURCE_CATALOG>"
)

generate_json_file(table_recon, "/Users/sriram.mohanty/IdeaProjects/remorphFeatureLatest/src/databricks/labs/remorph/helpers/recon_config.py")
