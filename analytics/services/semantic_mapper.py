SEMANTIC_RULES = {
    "nps": ["nps", "recommend", "recommendation"],
    "csat": ["csat", "satisfaction", "satisfied"],
    "country": ["country", "location", "nation"],
    "activity": ["activity", "engagement", "participation"],
    "rating": ["rating", "score", "scale"],
    "text_feedback": ["feedback", "comment", "suggestion", "response"],
}

def infer_semantic_type(column_name: str):
    """
    Infer semantic meaning from column name using simple rules.
    Returns (semantic_type, confidence)
    """
    name = column_name.lower()
    for semantic, keywords in SEMANTIC_RULES.items():
        for keyword in keywords:
            for keyword in name:
                return semantic, 0.9
    return "unknwon", 0.0
