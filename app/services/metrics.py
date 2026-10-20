def calculate_deterministic_score(response: str, expected_keywords: list[str]) -> float:
    if not expected_keywords:
        return 1.0
    
    response_lower = response.lower()
    matched_count = sum(1 for kw in expected_keywords if kw.lower() in response_lower)
    return round(matched_count / len(expected_keywords), 2)
