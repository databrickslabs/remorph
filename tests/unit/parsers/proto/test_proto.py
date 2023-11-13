import pathlib

from databricks.labs.remorph.parsers.proto import parse_proto

__folder__ = pathlib.Path(__file__).parent
__root__ = __folder__.parent.parent.parent.parent


def test_proto_ast():
    base_proto = __root__ / "src/databricks/labs/remorph/intermediate/proto/spark/connect/base.proto"
    proto = parse_proto(base_proto)
    assert proto is not None
