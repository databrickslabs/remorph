class ColumnMismatchException(Exception):
    """Raise the error when there is a mismatch in source and target column names"""


class DataSourceRuntimeException(Exception):
    """Raise the error when there is a runtime exception thrown in DataSource"""


class WriteToTableException(Exception):
    """Raise the error when there is a runtime exception thrown while writing data to table"""


class InvalidInputException(ValueError):
    """Raise the error when the input is invalid"""
