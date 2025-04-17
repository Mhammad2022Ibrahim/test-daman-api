import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.schemas import CreateAccount, UpdateAccount, CreateTransaction, ShowTransaction
from app.models import Account, Transaction
from uuid import uuid4
from random import randint

client = TestClient(app)

def test_all():
    account = CreateAccount(
        name="Khaled",
        email=f"khaled{uuid4().hex[:6]}@gmail.com",  # Randomized email
        phone=f"34567{randint(10000, 99999)}",         # Randomized phone
        balance=1000.0,
        address="Akkar"
    )
    response = client.post("/accounts/", json=account.model_dump())
    assert response.status_code == 200
    assert response.json()["message"].startswith("Account created successfully for")

    data = response.json()
    account_id = data["id"]  # <-- dynamic ID

    update_data = UpdateAccount(email=f"khaled_email_{account_id}_updated@gmail.com")
    
    update_response = client.put(f"/accounts/{account_id}", json=update_data.model_dump(exclude_unset=True))
    assert update_response.status_code == 200

    transaction = CreateTransaction(
        amount=90.0,
        transaction_type="deposit",
        account_id=account_id 
    )
    response = client.post("/transactions/", json=transaction.model_dump())
    assert response.status_code == 200

    response = client.get(f"/transactions/{account_id}?start_date=2025-01-01&end_date=2025-04-30")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_account():
    account = CreateAccount(
        name="Khaled",
        email=f"khaled{uuid4().hex[:6]}@gmail.com",  # Randomized email
        phone=f"96170{randint(10000, 99999)}",         # Randomized phone
        balance=1000.0,
        address="Akkar"
    )
    response = client.post("/accounts/", json=account.model_dump())
    assert response.status_code == 200
    assert response.json()["message"].startswith("Account created successfully for")


def test_duplicate_account():
    account = CreateAccount(
        name="mahmoud",
        email="zahraaibrahim13@gmail.com", 
        phone="9617033333",        
        balance=1000.0,
        address="Akkar"
    )
    response = client.post("/accounts/", json=account.model_dump())
    assert response.status_code == 400, response.json()
    assert response.json()["detail"] == "Account with this email already exists"

def test_update_account():
    account = UpdateAccount(
        email = "zahraaibrahim13@gmail.com"
    )
    # response = client.put("/accounts/3", json=account.model_dump())
    response = client.put("/accounts/3", json=account.model_dump(exclude_unset=True))
    assert response.status_code == 200

def test_create_transaction_deposit():
    transaction = CreateTransaction(
        amount = 100.0,
        transaction_type = "deposit",
        account_id = 3
    )
    response = client.post("/transactions/", json=transaction.model_dump())
    assert response.status_code == 200

def test_create_transaction_insufficient_balance():
    transaction = CreateTransaction(
        amount = 1000000.0,
        transaction_type = "withdrawal",
        account_id = 4
    )
    response = client.post("/transactions/", json=transaction.model_dump())
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"

def test_get_transactions():
    response = client.get("/transactions/3?start_date=2025-01-01&end_date=2025-04-30")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_transactions_not_find_account():
    response = client.get("/transactions/100?start_date=2025-01-01&end_date=2025-04-30")
    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Account not found"

def test_get_transactions_invalid_date_range():
    response = client.get("/transactions/3?start_date=2021-04-30&end_date=2024-01-01")
    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "No transactions found for this account in the given date range"