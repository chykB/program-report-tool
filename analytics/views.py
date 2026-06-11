from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from core.models import Cohort
from .services.ingestion import ingest_csv
from .models import Dataset, DatasetColumn, DataRow, Insight
from .serializers import (
    DatasetSerializer,
    DatasetColumnSerializer,
    DataRowSerializer,
    InsightSerializer,
)
from .services.ai_insight_service import generate_ai_insight


class DatasetUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, cohort_id, dataset_type):
        cohort = get_object_or_404(Cohort, id=cohort_id)
        file = request.FILES["file"]
        program = request.data.get("program") 
        if not program:
            return Response(
                {"error": "Program is required for dataset ingestion."},
                status=400
            )

        try:
            result = ingest_csv(
                file=file,
                cohort=cohort,
                program=program,
                dataset_type=dataset_type
            )
        except ValueError as error:
            return Response({"error": str(error)}, status=400)

        return Response(result)


class DatasetListView(APIView):
    def get(self, request):
        datasets = Dataset.objects.all().order_by("-uploaded_at")
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)


class DatasetDetailView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)


class DatasetColumnsView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        columns = DatasetColumn.objects.filter(dataset=dataset)
        serializer = DatasetColumnSerializer(columns, many=True)
        return Response(serializer.data)


class DatasetRowsView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        rows = DataRow.objects.filter(dataset=dataset)[:100]
        serializer = DataRowSerializer(rows, many=True)

        return Response({
            "dataset_id": dataset.id,
            "total_rows": DataRow.objects.filter(dataset=dataset).count(),
            "returned_rows": len(serializer.data),
            "rows": serializer.data,
        })


class DatasetInsightsView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        insights = Insight.objects.filter(dataset=dataset).order_by("-created_at")
        serializer = InsightSerializer(insights, many=True)
        return Response(serializer.data)

class GenerateAIInsightView(APIView):
    def post(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)

        try:
            result = generate_ai_insight(dataset)
        except ValueError as error:
            return Response({"error": str(error)}, status=400)
        except Exception as error:
            return Response(
                {"error": "AI insight generation failed.", "details": str(error)},
                status=500,
            )

        return Response(result)
