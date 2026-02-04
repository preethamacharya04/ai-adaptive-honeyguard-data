"""
ML Detector - Placeholder
Member 2 will implement the actual Isolation Forest here
"""


def get_ml_risk(behavioral_features):
    """
    Placeholder function
    Member 2 will replace this with actual ML model

    Args:
        behavioral_features: dict from extract_behavioral_features()
            {
                'requests_per_minute': float,
                'avg_time_gap': float,
                'session_duration': float,
                'unique_endpoints': int,
                'total_requests': int
            }

    Returns:
        int - risk score 0-100
    """
    # TEMPORARY: Simple rule-based risk until Member 2 provides ML model

    if behavioral_features is None:
        return 20  # Default low risk

    requests_per_min = behavioral_features.get('requests_per_minute', 0)
    session_duration = behavioral_features.get('session_duration', 0)
    total_requests = behavioral_features.get('total_requests', 0)

    risk = 0

    # High request frequency = suspicious
    if requests_per_min > 20:
        risk += 40
    elif requests_per_min > 10:
        risk += 25
    elif requests_per_min > 5:
        risk += 10

    # Very new session making lots of requests = suspicious
    if session_duration < 2 and total_requests > 10:
        risk += 30

    # Too many requests too fast
    avg_gap = behavioral_features.get('avg_time_gap', 10)
    if avg_gap < 1:  # Less than 1 second between requests
        risk += 30

    return min(risk, 100)

    # TODO for Member 2:
    # Replace above logic with:
    # 1. Load trained Isolation Forest model
    # 2. Transform behavioral_features into feature vector
    # 3. Get anomaly score from model
    # 4. Convert anomaly score to 0-100 risk score
    # 5. Return risk score
