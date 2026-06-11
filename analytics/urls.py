from django.urls import path
from .views import (
    DatasetUploadView,
    DatasetListView,
    DatasetDetailView,
    DatasetColumnsView,
    DatasetRowsView,
    DatasetInsightsView,
    GenerateAIInsightView,
)

urlpatterns = [
    path("upload/<int:cohort_id>/<str:dataset_type>/", DatasetUploadView.as_view(), name="dataset_upload"),
    
    path("datasets/", DatasetListView.as_view(), name="dataset_list"),
    path("datasets/<int:dataset_id>/", DatasetDetailView.as_view(), name="dataset_detail"),
    path("datasets/<int:dataset_id>/columns/", DatasetColumnsView.as_view(), name="dataset_columns"),
    path("datasets/<int:dataset_id>/rows/", DatasetRowsView.as_view(), name="dataset_rows"),
    path("datasets/<int:dataset_id>/insights/", DatasetInsightsView.as_view(), name="dataset_insights"),
    path("datasets/<int:dataset_id>/ai-insights/", GenerateAIInsightView.as_view(), name="generate_ai_insight"),

]
