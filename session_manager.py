"""
Session Manager
Tracks user sessions and behavioral data
"""

import time
import uuid
from datetime import datetime

# In-memory session storage (for demo)
sessions = {}


def create_session(user_id):
    """
    Create a new session for a user

    Args:
        user_id: str - Username or user identifier

    Returns:
        session_id: str - Unique session token
    """
    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        'user_id': user_id,
        'created_at': time.time(),
        'requests': [],
        'endpoints_accessed': [],
        'failed_attempts': 0,
        'initial_risk': 0
    }

    return session_id


def get_session(session_id):
    """
    Retrieve session data

    Args:
        session_id: str

    Returns:
        session data dict or None
    """
    return sessions.get(session_id)


def record_request(session_id, endpoint):
    """
    Record that a request was made

    Args:
        session_id: str
        endpoint: str - Which endpoint was accessed
    """
    if session_id in sessions:
        sessions[session_id]['requests'].append(time.time())
        sessions[session_id]['endpoints_accessed'].append(endpoint)


def get_request_frequency(session_id):
    """
    Calculate requests per minute for this session

    Args:
        session_id: str

    Returns:
        float - requests per minute
    """
    if session_id not in sessions:
        return 0

    current_time = time.time()
    session = sessions[session_id]

    # Count requests in last 60 seconds
    recent_requests = [
        req for req in session['requests']
        if current_time - req < 60
    ]

    return len(recent_requests)


def get_session_age(session_id):
    """
    Get how old this session is (in minutes)

    Args:
        session_id: str

    Returns:
        float - age in minutes
    """
    if session_id not in sessions:
        return 0

    created_at = sessions[session_id]['created_at']
    age_seconds = time.time() - created_at
    return age_seconds / 60


def extract_behavioral_features(session_id):
    """
    Extract features for ML model

    Args:
        session_id: str

    Returns:
        dict with behavioral features
    """
    if session_id not in sessions:
        return None

    session = sessions[session_id]

    # Calculate time gaps between requests
    requests = session['requests']
    if len(requests) > 1:
        gaps = [requests[i] - requests[i-1] for i in range(1, len(requests))]
        avg_gap = sum(gaps) / len(gaps) if gaps else 0
    else:
        avg_gap = 0

    return {
        'requests_per_minute': get_request_frequency(session_id),
        'avg_time_gap': avg_gap,
        'session_duration': get_session_age(session_id),
        'unique_endpoints': len(set(session['endpoints_accessed'])),
        'total_requests': len(requests)
    }
