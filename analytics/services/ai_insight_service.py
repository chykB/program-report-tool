import json
from statistics import mean

from django.conf import settings
from openai import OpenAI

from analytics.models import Dataset, DatasetColumn, DataRow, Insight


SENSITIVE_SEMANTIC_TYPES = {
    "person_name",
    "email",
}


def _safe_float(value):
    try:
        if value in [None, ""]:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _yes_count(values):
    yes_values = {"yes", "true", "1", "submitted", "passed", "active"}
    return sum(1 for value in values if str(value).strip().lower() in yes_values)


def build_dataset_summary(dataset: Dataset):
    columns = DatasetColumn.objects.filter(dataset=dataset)
    rows = DataRow.objects.filter(dataset=dataset)

    semantic_map = {
        column.semantic_type: column.raw_name
        for column in columns
        if column.semantic_type
    }

    summary = {
        "dataset_id": dataset.id,
        "dataset_type": dataset.dataset_type,
        "program": dataset.program,
        "cohort": str(dataset.cohort),
        "total_rows": rows.count(),
        "detected_columns": semantic_map,
        "metrics": {},
        "sample_rows": [],
    }

    row_data = [row.row_data for row in rows[:100]]

    for semantic_type, raw_name in semantic_map.items():
        if semantic_type in SENSITIVE_SEMANTIC_TYPES:
            continue

        values = [row.get(raw_name) for row in row_data if raw_name in row]
        numeric_values = [
            number for number in [_safe_float(value) for value in values]
            if number is not None
        ]

        if numeric_values:
            summary["metrics"][semantic_type] = {
                "average": round(mean(numeric_values), 2),
                "minimum": min(numeric_values),
                "maximum": max(numeric_values),
                "count": len(numeric_values),
            }

        if semantic_type in [
            "assignment_submitted",
            "assignment_passed",
            "is_active",
        ]:
            summary["metrics"][semantic_type] = {
                "yes_count": _yes_count(values),
                "total_count": len(values),
            }

    for row in row_data[:5]:
        clean_row = {}
        for key, value in row.items():
            matching_column = columns.filter(raw_name=key).first()

            if matching_column and matching_column.semantic_type in SENSITIVE_SEMANTIC_TYPES:
                continue

            clean_row[key] = value

        summary["sample_rows"].append(clean_row)

    return summary


def generate_fallback_mentor_insight(dataset_summary):
    metrics = dataset_summary.get("metrics", {})
    dataset_type = dataset_summary.get("dataset_type")
    total_rows = dataset_summary.get("total_rows", 0)

    risk_level = "low"
    findings = []
    actions = []

    nps_average = metrics.get("nps", {}).get("average")
    csat_average = metrics.get("csat", {}).get("average")

    if nps_average is not None:
        findings.append(f"Average NPS is {nps_average}.")
        if nps_average < 7:
            risk_level = "medium"
            actions.append("Follow up with learners who gave low recommendation scores.")

    if csat_average is not None:
        findings.append(f"Average CSAT is {csat_average}.")
        if csat_average < 7:
            risk_level = "medium"
            actions.append("Review learner support experience and identify recurring complaints.")

    active_metric = metrics.get("is_active")
    if active_metric:
        active_count = active_metric.get("yes_count", 0)
        total_count = active_metric.get("total_count", 0)

        if total_count:
            active_rate = round((active_count / total_count) * 100, 2)
            findings.append(f"{active_rate}% of learners were active in the previous week.")

            if active_rate < 60:
                risk_level = "high"
                actions.append("Prioritize outreach to inactive learners this week.")

    passed_metric = metrics.get("assignment_passed")
    if passed_metric:
        passed_count = passed_metric.get("yes_count", 0)
        total_count = passed_metric.get("total_count", 0)

        if total_count:
            pass_rate = round((passed_count / total_count) * 100, 2)
            findings.append(f"{pass_rate}% of tracked assignment records were passed.")

            if pass_rate < 60:
                risk_level = "high"
                actions.append("Organize a support session around the most difficult assignments.")

    if not findings:
        findings.append(
            f"The dataset contains {total_rows} rows, but no strong numeric risk signal was detected."
        )

    if not actions:
        actions.append("Continue monitoring learner engagement and support feedback.")

    return {
        "risk_level": risk_level,
        "summary": (
            f"This {dataset_type} dataset contains {total_rows} rows. "
            "The system generated mentor-focused recommendations from the available metrics."
        ),
        "key_findings": findings,
        "recommended_actions": actions,
        "mentor_message": (
            "Hi, I noticed some signals that may need support. "
            "Please let me know what has been challenging so we can work through it together."
        ),
    }

def generate_ai_insight(dataset: Dataset):
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not configured.")

    dataset_summary = build_dataset_summary(dataset)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # response = client.responses.create(
    #     model=settings.OPENAI_MODEL,
    #     instructions=(
    #         "You are an AI assistant for software engineering technical mentors. "
    #         "Analyze learner survey or activity data and return practical mentor actions. "
    #         "Do not invent data. Base your response only on the dataset summary provided."
    #     ),
    #     input=json.dumps(dataset_summary),
    #     text={
    #         "format": {
    #             "type": "json_schema",
    #             "name": "mentor_ai_insight",
    #             "strict": True,
    #             "schema": {
    #                 "type": "object",
    #                 "additionalProperties": False,
    #                 "properties": {
    #                     "risk_level": {
    #                         "type": "string",
    #                         "enum": ["low", "medium", "high"],
    #                     },
    #                     "summary": {
    #                         "type": "string",
    #                     },
    #                     "key_findings": {
    #                         "type": "array",
    #                         "items": {"type": "string"},
    #                     },
    #                     "recommended_actions": {
    #                         "type": "array",
    #                         "items": {"type": "string"},
    #                     },
    #                     "mentor_message": {
    #                         "type": "string",
    #                     },
    #                 },
    #                 "required": [
    #                     "risk_level",
    #                     "summary",
    #                     "key_findings",
    #                     "recommended_actions",
    #                     "mentor_message",
    #                 ],
    #             },
    #         }
    #     },
    # )

    # ai_result = json.loads(response.output_text)



    

    try:
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=(
                "You are an AI assistant for software engineering technical mentors. "
                "Analyze learner survey or activity data and return practical mentor actions. "
                "Do not invent data. Base your response only on the dataset summary provided."
            ),
            input=json.dumps(dataset_summary),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "mentor_ai_insight",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "risk_level": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                            },
                            "summary": {"type": "string"},
                            "key_findings": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "recommended_actions": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "mentor_message": {"type": "string"},
                        },
                        "required": [
                            "risk_level",
                            "summary",
                            "key_findings",
                            "recommended_actions",
                            "mentor_message",
                        ],
                    },
                }
            },
        )

        ai_result = json.loads(response.output_text)
        source = "openai"

    except Exception:
        ai_result = generate_fallback_mentor_insight(dataset_summary)
        source = "fallback"

    insight = Insight.objects.create(
        dataset=dataset,
        insight_type="ai_summary",
        dimension="mentor_recommendation",
        value=ai_result,
    )

    return {
        "insight_id": insight.id,
        "source": source,
        "dataset": {
            "id": dataset.id,
            "cohort": str(dataset.cohort),
            "program": dataset.program,
            "dataset_type": dataset.dataset_type,
            "original_filename": dataset.original_filename,
            "row_count": dataset.row_count,
            "column_count": dataset.column_count,
        },
        "ai_insight": ai_result,
    }