import io
import hashlib
import pandas as pd
from django.db import transaction
from ..models import Dataset, DatasetColumn, DataRow
from .semantic_service import apply_semantic_detection

def ingest_csv(file, cohort, dataset_type, program):
    """
    Ingest a CSV file:
    - Prevent duplicate ingestion (same file_hash)
    - Create Dataset, DatasetColumn, DataRow
    - Apply semantic detection (MVP rules)
    """

    allowed_types = [choice[0] for choice in Dataset.DATASET_TYPE]
    if dataset_type not in allowed_types:
        raise ValueError(f"Invalid dataset_type: {dataset_type}. Must be one of the allowed types")
    

    allowed_programs = [choice[0] for choice in Dataset.PROGRAMS]
    if program not in allowed_programs:
        raise ValueError(
            f"Invalid program: {program}. Must be one of: {', '.join(allowed_programs)}"
        )

    
    file_bytes = file.read()
    file_hash = hashlib.md5(file_bytes).hexdigest()
    file.seek(0)

    if Dataset.objects.filter(cohort=cohort, program=program, dataset_type=dataset_type, file_hash=file_hash).exists():
        return {"error": "This file has already been uploaded"}

    text_file = io.TextIOWrapper(file.file, encoding="utf-8-sig")
    df = pd.read_csv(
        text_file,
        sep=None,
        engine="python",
        on_bad_lines="skip"
    )
    df.dropna(how="all", inplace=True)
    if df.empty:
        raise ValueError("CSV contains no valid rows")
    
    dataset = Dataset.objects.create(
        cohort=cohort,
        program=program,
        dataset_type=dataset_type,
        source="csv",
        file_hash=file_hash,
        original_filename=getattr(file, "name", ""),
        row_count=len(df),
        column_count=len(df.columns),
    )

    for col in df.columns:
        DatasetColumn.objects.create(dataset=dataset, raw_name=col)

    rows_to_create = []
    for record in df.to_dict(orient="records"):
        clean_record = {}
        for k, v in record.items():
            if pd.isna(v):
                clean_record[k] = None
            elif isinstance(v, (pd.Timestamp, pd.Timedelta)):
                clean_record[k] = str(v)
            elif isinstance(v, (pd.Int64Dtype, pd.Float64Dtype)):
                clean_record[k] = float(v)
            else:
                clean_record[k] = v
        rows_to_create.append(DataRow(dataset=dataset, row_data=clean_record))
        # rows = [DataRow(dataset=dataset, row_data=row) for row in df.to_dict(orient="records")]
    DataRow.objects.bulk_create(rows_to_create)

    apply_semantic_detection(dataset)
    return {
        "status": "success",
        "dataset_id": dataset.pk,
        "original_filename": dataset.original_filename,
        "rows_ingested": len(rows_to_create),
        "columns_ingested": len(df.columns),
        "columns": list(df.columns),
        
    }
