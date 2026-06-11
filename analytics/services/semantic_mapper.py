def normalize(text: str) -> str:
    return text.lower().strip()

SURVEY_RULES = {
    "nps": ["nps", "recommend",],
    "csat": ["csat", "satisfaction", "tech support",],
    "community_engagement": ["community event", "community interaction",],
    "learning_experience": ["learning activity", "learning activities",],
    "coordination": ["coordination", "cordination",],
    "retention": ["retention"],
    
}
LEARNER_ACTIVITY_RULES = {
    "person_name": ["full name", "name",],
    "email": ["email"],
    "country": ["country"],
    "age": ["age"],
    "age_range": ["age range"],
    "cohort": ["cohort"],
    "student_status": ["student status", "student_status"],
    "enrollment_status": ["enrollment", "activated"],
    "is_active": ["active previous week", "is_active"],
    "assignment_name": ["assignment name"],
    "assignment_score": ["assignment score"],
    "assignment_type": ["assignment type"],
    "assignment_submitted": ["assignment submitted", "submitted"],
    "assignment_passed": ["passed", "assignment passed"],
    "assignment_resubmitted": ["resubmitted"],
    "activity_count": ["no of assignment", "number of assignment"],
    "drop_off_reason": ["drop off reason", "drop off"],
}

def infer_semantic_type(column_name: str, dataset_type: str):
    name = normalize(column_name)
    if dataset_type == "survey":
        rules = SURVEY_RULES
    elif dataset_type == "learner_activities":
        rules = LEARNER_ACTIVITY_RULES
    else:
        return None, 0.0
    
    for semantic, keywords in rules.items():
        for keyword in keywords:
            if keyword in name:
                return semantic, 0.9
    return None, 0.0








# SEMANTIC_RULES = {
#     "nps": ["nps", "recommend", "recommendation"],
#     "csat": ["csat", "satisfaction", "satisfied"],
#     "country": ["country", "location", "nation"],
#     "activit:y": ["activity", "engagement", "participation"],
#     "rating": ["rating", "score", "scale"],
#     "text_feedback": ["feedback", "comment", "suggestion", "response"],
# }

# def infer_semantic_type(column_name: str):
#     """
#     Infer semantic meaning from column name using simple rules.
#     Returns (semantic_type, confidence)
#     """
#     name = column_name.lower()
#     for semantic, keywords in SEMANTIC_RULES.items():
#         for keyword in keywords:
#             for keyword in name:
#                 return semantic, 0.9
#     return "unknwon", 0.0
