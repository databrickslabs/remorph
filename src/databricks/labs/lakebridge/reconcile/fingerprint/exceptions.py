"""Exception hierarchy for the fingerprint module."""


class FingerprintError(Exception):
    """Base for errors raised by the fingerprint module."""


class UnsupportedDataSourceError(FingerprintError, ValueError):
    """No registered FingerprintQueryBuilder for the requested data source."""


class UnmappedTargetColumnMappingError(FingerprintError):
    """A ``column_mapping`` entry references a target name that doesn't exist on the target."""
