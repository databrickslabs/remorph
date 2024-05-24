class ColumnMismatchException(Exception):
    """Raise the error when there is a mismatch in source and target column names"""


class DataSourceRuntimeException(Exception):
    """Raise the error when there is a runtime exception thrown in DataSource"""


class WriteToTableException(Exception):
    """Raise the error when there is a runtime exception thrown while writing data to table"""


class InvalidReportTypeException(ValueError):
    """Raise the error when the input report type is invalid"""
