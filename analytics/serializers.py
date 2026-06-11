from rest_framework import serializers
from .models import Dataset, DatasetColumn, DataRow, Insight


class DatasetSerializer(serializers.ModelSerializer):
    cohort_name = serializers.CharField(source="cohort.name", read_only=True)

    class Meta:
        model = Dataset
        fields = [
            "id",
            "cohort",
            "cohort_name",
            "program",
            "dataset_type",
            "source",
            "file_hash",
            "original_filename",
            "row_count",
            "column_count",
            "uploaded_at",
        ]


class DatasetColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetColumn
        fields = [
            "id",
            "dataset",
            "raw_name",
            "semantic_type",
            "confidence",
        ]


class DataRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRow
        fields = [
            "id",
            "dataset",
            "row_data",
        ]


class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = [
            "id",
            "dataset",
            "insight_type",
            "dimension",
            "value",
            "created_at",
        ]