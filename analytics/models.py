from django.db import models
from core.models import Cohort

class Dataset(models.Model):
    DATASET_TYPE = (
        ("survey", "survey"),
        ("learner_activities", "Learner Activities"),
    )
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    dataset_type = models.CharField(max_length=30, choices=DATASET_TYPE)
    source = models.CharField(max_length=30, default="csv")
    file_hash = models.CharField(max_length=64, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        type_display = dict(self.DATASET_TYPE).get(self.dataset_type, self.dataset_type)
        return f"{self.cohort} - {type_display}"

class DatasetColumn(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='analytics_datasets')
    raw_name = models.CharField(max_length=255)
    semantic_type = models.CharField(max_length=50, unique=True, null=True, blank=True)
    confidence = models.FloatField(default=0.0)

class DataRow(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    row_data = models.JSONField()

class Insight(models.Model):
    INSIGHT_TYPES = (
        ("nps", "NPS"),
        ("csat", "CSAT"),
        ("distribution", "Distribution"),
        ("summary", "Summary"),
    )
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    insight_type = models.CharField(max_length=30, choices=INSIGHT_TYPES)
    dimension =models.CharField(max_length=100, null=True, blank=True)
    value = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dataset} - {self.insight_type}"