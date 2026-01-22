from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from core.models import Cohort
from .services.ingestion import ingest_csv

class DatasetUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, cohort_id, dataset_type):
        cohort = get_object_or_404(Cohort, id=cohort_id)
        file = request.FILES["file"]

        result = ingest_csv(
            file=file,
            cohort=cohort,
            dataset_type=dataset_type
        )

        return Response(result)