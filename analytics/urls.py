from django.urls import path
from .views import DatasetUploadView

urlpatterns = [
    path("upload/<int:cohort_id>/<str:dataset_type>/", DatasetUploadView.as_view(), name="dataset_upload")

]