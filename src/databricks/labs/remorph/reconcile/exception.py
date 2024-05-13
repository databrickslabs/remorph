class ColumnMismatchException(Exception):
    """Raise the error when there is a mismatch in source and target column names"""


class MockDataNotAvailableException(Exception):
    """Raise the error when there is no mock available for the given inputs"""
