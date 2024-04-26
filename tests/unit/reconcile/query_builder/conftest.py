import pytest
from sqlglot import parse_one

from databricks.labs.remorph.reconcile.recon_config import Schema


@pytest.fixture
def schema():
    sch = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    sch_with_alias = [
        Schema("s_suppkey_t", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address_t", "varchar"),
        Schema("s_nationkey_t", "number"),
        Schema("s_phone_t", "varchar"),
        Schema("s_acctbal_t", "number"),
        Schema("s_comment_t", "varchar"),
    ]

    return sch, sch_with_alias


@pytest.fixture
def expr():
    return parse_one("SELECT col1 FROM DUAL")
