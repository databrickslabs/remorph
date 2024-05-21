class ColumnMismatchException(Exception):
    """Raise the error when there is a mismatch in source and target column names"""


class DataSourceRuntimeException(Exception):
    """Raise the error when there is a runtime exception thrown in DataSource"""
