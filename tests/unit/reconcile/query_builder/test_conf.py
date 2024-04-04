from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Filters,
    JdbcReaderOptions,
    Schema,
    Table,
    Thresholds,
    Transformation,
)


class TestConf:
    @property
    def get_schema(self):
        return [
            Schema("s_suppkey", "number"),
            Schema("s_name", "varchar"),
            Schema("s_address", "varchar"),
            Schema("s_nationkey", "number"),
            Schema("s_phone", "varchar"),
            Schema("s_acctbal", "number"),
            Schema("s_comment", "varchar"),
        ]

    @property
    def get_alias_schema(self):
        return [
            Schema("s_suppkey_t", "number"),
            Schema("s_name", "varchar"),
            Schema("s_address_t", "varchar"),
            Schema("s_nationkey_t", "number"),
            Schema("s_phone_t", "varchar"),
            Schema("s_acctbal_t", "number"),
            Schema("s_comment_t", "varchar"),
        ]

    @property
    def get_table_conf_default(self):
        return Table(source_name="supplier", target_name="supplier")

    @property
    def get_table_conf_all_options(self):
        return Table(
            source_name="supplier",
            target_name="target_supplier",
            jdbc_reader_options=JdbcReaderOptions(
                number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
            ),
            join_columns=["s_suppkey"],
            select_columns=["s_suppkey", "s_name", "s_address"],
            drop_columns=["s_comment"],
            column_mapping=[
                ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
                ColumnMapping(source_name="s_address", target_name="s_address_t"),
            ],
            transformations=[
                Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
                Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone)"),
                Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
            ],
            thresholds=[Thresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int")],
            filters=Filters(source="s_name='t' and s_address='a'", target="s_name='t' and s_address_t='a'"),
        )
