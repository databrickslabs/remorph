import pytest
from unittest.mock import Mock
from databricks.labs.remorph.discovery.table import TableDefinition
from databricks.labs.remorph.discovery.tsql_table_definition import TsqlTableDefinitionService


@pytest.fixture
def mock_cursor():
    cursor = Mock()
    cursor.description = [
        ('TABLE_CATALOG',),
        ('TABLE_SCHEMA',),
        ('TABLE_NAME',),
        ('location',),
        ('TABLE_FORMAT',),
        ('view_definition',),
        ('DERIVED_SCHEMA',),
        ('SIZE_GB',),
        ('TABLE_COMMENT',),
        ('PK_COLUMN_NAME',),
    ]
    return cursor


def test_get_table_definition_with_data(mock_cursor):
    """Test with sample table data"""

    mock_cursor.execute.return_value = [
        (
            'test_catalog',
            'dbo',
            'test_table',
            '/path/to/location',
            'ROWS',
            '',
            'id§int§false§test comment‡name§varchar(50)§true§',
            1.5,
            'Table Comment',
            'id',
        )
    ]
    tss = TsqlTableDefinitionService(mock_cursor)

    result = list(tss.get_table_definition("test_catalog"))
    assert isinstance(result[0], TableDefinition)
    assert result[0].fqn.catalog == 'test_catalog'
    assert result[0].fqn.schema == 'dbo'
    assert result[0].fqn.name == 'test_table'
    assert len(result[0].columns) == 2
    assert result[0].primary_keys == ['id']


def test_get_table_definition_with_composite_pk(mock_cursor):
    mock_cursor.execute = Mock(
        return_value=[
            (
                'test_catalog',
                'dbo',
                'test_table',
                '/path/to/location',
                'ROWS',
                '',
                'id§int§false§‡order_id§int§false§',
                1.5,
                'Table Comment',
                'id:order_id',
            )
        ]
    )
    mock_cursor.return_value = mock_cursor

    tss = TsqlTableDefinitionService(mock_cursor)
    result = list(tss.get_table_definition("test_catalog"))
    assert result[0].primary_keys == ['id', 'order_id']
    mock_cursor.close.assert_called_once()
