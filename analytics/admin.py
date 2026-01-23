from django.contrib import admin
from .models import Dataset, DatasetColumn, DataRow, Insight

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("id", "cohort", "dataset_type", "uploaded_at")
    list_filter = ("dataset_type", "cohort")

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