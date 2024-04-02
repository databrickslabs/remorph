from databricks.labs.remorph.reconcile.recon_config import Schema

schema = [
    Schema("s_suppkey", "number"),
    Schema("s_name", "varchar"),
    Schema("s_address", "varchar"),
    Schema("s_nationkey", "number"),
    Schema("s_phone", "varchar"),
    Schema("s_acctbal", "number"),
    Schema("s_comment", "varchar"),
]


alias_schema = [
    Schema("s_suppkey_t", "number"),
    Schema("s_name", "varchar"),
    Schema("s_address_t", "varchar"),
    Schema("s_nationkey_t", "number"),
    Schema("s_phone_t", "varchar"),
    Schema("s_acctbal_t", "number"),
    Schema("s_comment_t", "varchar"),
]
