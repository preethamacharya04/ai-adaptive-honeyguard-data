"""
Data Handler - Placeholder
Member 3 will implement real customer data functions here
"""


def get_real_customer(customer_id):
    """
    Placeholder - Member 3 will implement with real 5 customers

    Args:
        customer_id: int - Customer ID (1001-1005)

    Returns:
        dict - Real customer data
    """
    # TEMPORARY: Dummy data
    # Member 3 will replace with actual 5 real customers

    return {
        "id": customer_id,
        "name": "John Smith",
        "email": "john.smith@techcorp.com",
        "phone": "+1-555-0101",
        "ssn": "123-45-6789",
        "account_balance": 125000.50,
        "credit_score": 750,
        "address": "123 Main St, San Francisco, CA 94102",
        "date_of_birth": "1980-03-15",
        "account_created": "2018-01-10",
        "last_login": "2026-02-03T10:15:42Z",
        "account_type": "Premium Business",
        "status": "Active",
        "transaction_count": 2134,
        "avg_monthly_spend": 9250.75,
        "kyc_verified": True,
        "risk_category": "Low",
        "contact_preference": "email",
        "timezone": "America/Los_Angeles",
        "two_factor_enabled": True
    }


def get_randomized_real_data(customer_id):
    """
    Placeholder - Member 3 will implement
    Returns real data with slight modifications (for medium-risk users)

    Args:
        customer_id: int

    Returns:
        dict - Real customer data with randomization
    """
    import random

    real_data = get_real_customer(customer_id)

    # Add slight randomization to balance
    real_data['account_balance'] += random.uniform(-100, 100)
    real_data['account_balance'] = round(real_data['account_balance'], 2)

    return real_data


def get_real_transactions(customer_id, limit=10):
    """
    Placeholder - Member 3 will implement
    Returns real transaction history

    Args:
        customer_id: int
        limit: int - Number of transactions to return

    Returns:
        list of transaction dicts
    """
    # TEMPORARY: Dummy transactions
    # Member 3 will replace with real transaction data

    return [
        {
            "transaction_id": "TXN-20250203-001",
            "customer_id": customer_id,
            "date": "2025-02-03",
            "time": "14:30:22",
            "type": "debit",
            "description": "Amazon Purchase",
            "amount": -89.99,
            "balance_after": 125000.50,
            "merchant": "Amazon.com",
            "category": "Shopping"
        },
        {
            "transaction_id": "TXN-20250202-045",
            "customer_id": customer_id,
            "date": "2025-02-02",
            "time": "09:15:00",
            "type": "credit",
            "description": "Salary Deposit",
            "amount": 5000.00,
            "balance_after": 125090.49,
            "merchant": "ABC Corporation",
            "category": "Income"
        }
    ]
