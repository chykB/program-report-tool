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
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        type_display = dict(self.DATASET_TYPE).get(self.dataset_type, self.dataset_type)
        return f"{self.cohort} - {type_display}"

class DatasetColumn(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    raw_name = models.CharField(max_length=255)
    semantic_type = models.CharField(max_length=50, null=True, blank=True)
    confidence = models.FloatField(default=0.0)

class DataRow(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    row_data = models.JSONField()