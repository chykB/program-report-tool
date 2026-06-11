from django.contrib import admin
from .models import Dataset, DatasetColumn, DataRow, Insight

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cohort",
        "program",
        "dataset_type",
        "original_filename",
        "row_count",
        "column_count",
        "uploaded_at",
    )
    list_filter = ("dataset_type", "program", "cohort")
    search_fields = ("original_filename", "file_hash", "cohort__name")
    

@admin.register(DatasetColumn)
class DatasetColunmAdmin(admin.ModelAdmin):
    list_display = ("id", "dataset", "raw_name", "semantic_type", "confidence")

@admin.register(DataRow)
class DataRowAdmin(admin.ModelAdmin):
    list_display = ("id", "dataset")
    readonly_fields = ("row_data",)

@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ("id", "dataset", "insight_type", "created_at")