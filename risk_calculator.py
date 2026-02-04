"""
Risk Calculator
Combines different risk signals into final risk score
"""

from session_manager import extract_behavioral_features


def calculate_initial_risk(user_data, request_metadata):
    """
    Calculate risk at registration/login time

    Args:
        user_data: dict with email, name
        request_metadata: dict with user_agent, ip, etc.

    Returns:
        int - risk score 0-100
    """
    risk = 0

    # 1. Email Analysis (0-30 points)
    email = user_data.get('email', '').lower()

    suspicious_domains = [
        'tempmail.com', 'guerrillamail.com', '10minutemail.com',
        'throwaway.email', 'mailinator.com', 'trashmail.com',
        'fakeinbox.com', 'yopmail.com'
    ]

    if any(domain in email for domain in suspicious_domains):
        risk += 30

    # Check for random-looking email
    username_part = email.split('@')[0]
    digit_count = sum(c.isdigit() for c in username_part)
    if digit_count > 5:
        risk += 15

    # 2. Name Analysis (0-15 points)
    name = user_data.get('name', '').lower()

    suspicious_words = ['test', 'admin',
                        'hacker', 'bot', 'script', 'auto', 'fake']
    if any(word in name for word in suspicious_words):
        risk += 15

    # 3. User Agent Analysis (0-25 points)
    user_agent = request_metadata.get('user_agent', '').lower()

    automated_tools = ['python', 'curl', 'wget',
                       'postman', 'httpie', 'bot', 'scrapy']
    if any(tool in user_agent for tool in automated_tools):
        risk += 25
    elif len(user_agent) < 10:
        risk += 20

    # 4. Account age check (if available)
    account_age_days = user_data.get('account_age_days', 999)
    if account_age_days < 7:
        risk += 10

    return min(risk, 100)


def calculate_final_risk(session_id, ml_risk_score):
    """
    Combine initial risk + ML risk into final risk

    Args:
        session_id: str
        ml_risk_score: int (0-100) from Member 2's ML model

    Returns:
        int - final risk score 0-100
    """
    from session_manager import get_session

    session = get_session(session_id)
    if not session:
        return 50  # Default if session not found

    initial_risk = session.get('initial_risk', 0)

    # Weighted combination
    # 60% initial risk, 40% behavioral (ML) risk
    final_risk = (initial_risk * 0.6) + (ml_risk_score * 0.4)

    return int(final_risk)


def determine_data_source(risk_score):
    """
    Decide which data to serve based on risk

    Args:
        risk_score: int (0-100)

    Returns:
        str - 'real', 'randomized', or 'honey'
    """
    if risk_score < 35:
        return 'real'
    elif risk_score < 70:
        return 'randomized'
    else:
        return 'honey'
