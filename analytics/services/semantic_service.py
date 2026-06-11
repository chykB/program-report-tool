from analytics.models import Dataset, DatasetColumn
from .semantic_mapper import infer_semantic_type

def apply_semantic_detection(dataset: Dataset):
    """
    Detect semantic meaning for all columns in a dataset.
    """
    columns = DatasetColumn.objects.filter(dataset=dataset)
    updated = 0
    for column in columns:
        semantic, confidence = infer_semantic_type(
            column.raw_name, 
            column.dataset.dataset_type
            )
        column.semantic_type = semantic
        column.confidence = confidence
        column.save(
            update_fields=[
                "semantic_type", 
                "confidence"
                ])
        updated += 1
    return {
        "dataset_id": dataset.pk,
        "column_updated": updated
    }