"""
Honey Data Generator - Placeholder
Member 3 will implement AI-generated fake data here
"""

import random
from datetime import datetime, timedelta


def generate_honey_customer(customer_id):
    """
    Placeholder - Member 3 will implement with AI generation

    Args:
        customer_id: int

    Returns:
        dict - Fake but realistic customer data
    """
    # TEMPORARY: Simple fake data
    # Member 3 will replace with AI-generated realistic fake data

    fake_names = ["Robert Johnson", "Michael Williams",
                  "David Brown", "James Davis"]
    fake_emails = [
        "user12345@tempmail.com",
        "test_account@guerrillamail.com",
        "random4567@10minutemail.com"
    ]

    return {
        "id": customer_id,
        "name": random.choice(fake_names),
        "email": random.choice(fake_emails),
        "phone": f"+1-555-{random.randint(1000, 9999)}",
        "ssn": f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}",
        "account_balance": round(random.uniform(10000, 150000), 2),
        "credit_score": random.randint(600, 800),
        "address": f"{random.randint(100, 9999)} Fake St, Decoy City, XX {random.randint(10000, 99999)}",
        "date_of_birth": f"{random.randint(1970, 1995)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "account_created": f"{random.randint(2015, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "last_login": datetime.now().isoformat() + "Z",
        "account_type": random.choice(["Premium Business", "Standard", "Basic"]),
        "status": "Active",
        "transaction_count": random.randint(500, 3000),
        "avg_monthly_spend": round(random.uniform(5000, 15000), 2),
        "kyc_verified": True,
        "risk_category": "Low",
        "contact_preference": "email",
        "timezone": random.choice(["America/New_York", "America/Los_Angeles", "America/Chicago"]),
        "two_factor_enabled": random.choice([True, False])
    }


def generate_honey_transactions(customer_id, limit=10):
    """
    Placeholder - Member 3 will implement with AI generation

    Args:
        customer_id: int
        limit: int - Number of fake transactions

    Returns:
        list of fake transaction dicts
    """
    # TEMPORARY: Simple fake transactions
    # Member 3 will replace with AI-generated realistic fake transactions

    fake_merchants = [
        "Netflix Subscription",
        "Starbucks Coffee",
        "Shell Gas Station",
        "Walmart Supercenter",
        "Target Store",
        "McDonald's",
        "Best Buy Electronics"
    ]

    fake_transactions = []

    for i in range(limit):
        transaction_date = datetime.now() - timedelta(days=i)

        fake_transactions.append({
            "transaction_id": f"TXN-FAKE-{random.randint(10000, 99999)}",
            "customer_id": customer_id,
            "date": transaction_date.strftime("%Y-%m-%d"),
            "time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}",
            "type": random.choice(["debit", "credit"]),
            "description": random.choice(fake_merchants),
            "amount": round(random.uniform(-500, 1000), 2),
            "balance_after": round(random.uniform(10000, 150000), 2),
            "merchant": random.choice(fake_merchants),
            "category": random.choice(["Shopping", "Food", "Gas", "Entertainment", "Bills"])
        })

    return fake_transactions
