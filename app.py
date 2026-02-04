"""
HoneyGuard Backend - Main Application
Member 1: Core Backend + Decision Engine
"""

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import uvicorn

# Import your modules
from session_manager import (
    create_session,
    get_session,
    record_request,
    extract_behavioral_features
)
from risk_calculator import (
    calculate_initial_risk,
    calculate_final_risk,
    determine_data_source
)
from ml_detector import get_ml_risk
from data_handler import (
    get_real_customer,
    get_randomized_real_data,
    get_real_transactions
)
from honey_generator import (
    generate_honey_customer,
    generate_honey_transactions
)

app = FastAPI(title="HoneyGuard Banking API", version="1.0")


# Request/Response Models
class LoginRequest(BaseModel):
    customer_id: int  # 1001-1005
    email: str
    password: str


class LoginResponse(BaseModel):
    session_id: str
    message: str
    customer_name: str


# -------------------------------------------------------------------
# ENDPOINT 1: Login
# -------------------------------------------------------------------

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, http_request: Request):
    """
    Customer login endpoint
    Creates session and calculates initial risk
    """

    # Extract metadata
    user_agent = http_request.headers.get("user-agent", "Unknown")

    # For demo: We accept any password (skip real authentication)
    # In production, verify password here

    # Get real customer data to extract name
    customer_data = get_real_customer(request.customer_id)

    user_data = {
        'email': request.email,
        'name': customer_data.get('name', 'Unknown'),
        'customer_id': request.customer_id
    }

    request_metadata = {
        'user_agent': user_agent,
        'ip': http_request.client.host if http_request.client else 'Unknown'
    }

    # Calculate initial risk
    initial_risk = calculate_initial_risk(user_data, request_metadata)

    # Create session
    session_id = create_session(str(request.customer_id))

    # Store initial risk in session
    session = get_session(session_id)
    session['initial_risk'] = initial_risk
    session['customer_id'] = request.customer_id

    print(f"\n{'='*60}")
    print(f"✅ LOGIN SUCCESSFUL")
    print(f"{'='*60}")
    print(f"Customer: {customer_data.get('name')} (ID: {request.customer_id})")
    print(f"Email: {request.email}")
    print(f"User-Agent: {user_agent[:50]}...")
    print(f"Initial Risk Score: {initial_risk}/100")
    print(f"Session ID: {session_id}")
    print(f"{'='*60}\n")

    return {
        'session_id': session_id,
        'message': 'Login successful',
        'customer_name': customer_data.get('name', 'Customer')
    }


# -------------------------------------------------------------------
# ENDPOINT 2: Get Customer Account Data
# -------------------------------------------------------------------

@app.get("/account")
def get_account(session_id: str = Header(..., alias="X-Session-ID")):
    """
    Get customer account information
    Routes to real/randomized/honey data based on risk
    """

    # Validate session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session ID")

    # Record this request
    record_request(session_id, '/account')

    # Extract behavioral features
    features = extract_behavioral_features(session_id)

    # Get ML risk score (Member 2's function)
    ml_risk = get_ml_risk(features)

    # Calculate final risk
    final_risk = calculate_final_risk(session_id, ml_risk)

    # Determine data source
    data_source = determine_data_source(final_risk)

    # Route to appropriate data
    customer_id = session.get('customer_id', 1001)

    if data_source == 'real':
        account_data = get_real_customer(customer_id)  # Member 3's function
    elif data_source == 'randomized':
        account_data = get_randomized_real_data(
            customer_id)  # Member 3's function
    else:  # honey
        account_data = generate_honey_customer(
            customer_id)  # Member 3's function

    print(f"\n{'='*60}")
    print(f"📊 ACCOUNT REQUEST")
    print(f"{'='*60}")
    print(f"Customer ID: {customer_id}")
    print(f"Session ID: {session_id[:20]}...")
    print(f"Behavioral Features:")
    print(f"  - Requests/min: {features.get('requests_per_minute', 0)}")
    print(f"  - Session age: {features.get('session_duration', 0):.1f} min")
    print(f"  - Total requests: {features.get('total_requests', 0)}")
    print(f"Risk Scores:")
    print(f"  - Initial Risk: {session.get('initial_risk', 0)}/100")
    print(f"  - ML Risk: {ml_risk}/100")
    print(f"  - FINAL RISK: {final_risk}/100")
    print(f"Data Source: {data_source.upper()}")
    print(f"{'='*60}\n")

    # Return data with risk info (for demo/dashboard)
    return {
        **account_data,
        "_risk_score": final_risk,
        "_data_source": data_source,
        "_ml_risk": ml_risk,
        "_initial_risk": session.get('initial_risk', 0)
    }


# -------------------------------------------------------------------
# ENDPOINT 3: Get Transaction History
# -------------------------------------------------------------------

@app.get("/transactions")
def get_transactions(
    session_id: str = Header(..., alias="X-Session-ID"),
    limit: int = 10
):
    """
    Get customer transaction history
    Routes to real/honey data based on risk
    """

    # Validate session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session ID")

    # Record request
    record_request(session_id, '/transactions')

    # Get features
    features = extract_behavioral_features(session_id)

    # Get ML risk
    ml_risk = get_ml_risk(features)

    # Calculate final risk
    final_risk = calculate_final_risk(session_id, ml_risk)

    # Determine source
    data_source = determine_data_source(final_risk)

    # Route data
    customer_id = session.get('customer_id', 1001)

    if data_source == 'honey':
        transactions = generate_honey_transactions(customer_id, limit)
    else:
        transactions = get_real_transactions(customer_id, limit)

    print(f"\n📋 TRANSACTIONS REQUEST")
    print(f"Customer ID: {customer_id}")
    print(f"Final Risk: {final_risk}/100")
    print(f"Data Source: {data_source.upper()}")
    print(f"Returning {len(transactions)} transactions\n")

    return {
        'transactions': transactions,
        'count': len(transactions),
        '_risk_score': final_risk,
        '_data_source': data_source
    }


# -------------------------------------------------------------------
# ENDPOINT 4: Get Balance (Quick Check)
# -------------------------------------------------------------------

@app.get("/balance")
def get_balance(session_id: str = Header(..., alias="X-Session-ID")):
    """
    Quick balance check
    """

    # Validate session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session ID")

    # Record request
    record_request(session_id, '/balance')

    # Get features
    features = extract_behavioral_features(session_id)

    # Get risks
    ml_risk = get_ml_risk(features)
    final_risk = calculate_final_risk(session_id, ml_risk)
    data_source = determine_data_source(final_risk)

    # Route data
    customer_id = session.get('customer_id', 1001)

    if data_source == 'real':
        account = get_real_customer(customer_id)
    elif data_source == 'randomized':
        account = get_randomized_real_data(customer_id)
    else:
        account = generate_honey_customer(customer_id)

    return {
        'balance': account.get('account_balance', 0),
        'currency': 'USD',
        '_risk_score': final_risk,
        '_data_source': data_source
    }


# -------------------------------------------------------------------
# ENDPOINT 5: Health Check
# -------------------------------------------------------------------

@app.get("/")
def root():
    """
    Health check endpoint
    """
    return {
        'status': 'online',
        'service': 'HoneyGuard Banking API',
        'version': '1.0',
        'endpoints': [
            'POST /login',
            'GET /account',
            'GET /transactions',
            'GET /balance'
        ]
    }


# -------------------------------------------------------------------
# Run Server
# -------------------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 HONEYGUARD BANKING API")
    print("="*60)
    print("📍 Server: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("="*60)
    print("\nRisk Thresholds:")
    print("  🟢 0-34: Real data (low risk)")
    print("  🟡 35-69: Randomized real data (medium risk)")
    print("  🔴 70-100: Honey data (high risk - attacker)")
    print("="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
