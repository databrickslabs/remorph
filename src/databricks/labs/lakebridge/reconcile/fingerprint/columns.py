from dataclasses import dataclass

from databricks.labs.lakebridge.reconcile.recon_config import Schema


@dataclass
class DetectionColumn(Schema):
    """A detection column that also carries the type of its column on the other side."""

    counterpart_type: str | None = None


def counterpart_type_of(column: Schema) -> str | None:
    return column.counterpart_type if isinstance(column, DetectionColumn) else None


def pair_detection_columns(source_cols: list[Schema], target_cols: list[Schema]) -> tuple[list[Schema], list[Schema]]:
    """Attach each side's counterpart type; both lists are in the same source-canonical order."""
    paired_source: list[Schema] = [
        DetectionColumn(s.ansi_normalized_column_name, s.data_type, s.source_normalized_column_name, t.data_type)
        for s, t in zip(source_cols, target_cols)
    ]
    paired_target: list[Schema] = [
        DetectionColumn(t.ansi_normalized_column_name, t.data_type, t.source_normalized_column_name, s.data_type)
        for s, t in zip(source_cols, target_cols)
    ]
    return paired_source, paired_target
