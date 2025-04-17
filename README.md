# FastAPI Test Damamn API

This project provides a simple RESTful API for managing accounts and their transactions using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## Features

- Creating accounts
- Updating account details
- Creating deposit and withdrawal transactions
- Viewing transactions by date range

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.11+
- `pip` or `pipenv`
- (Optional) `virtualenv` for environment isolation
- `.env` file with a valid `DATABASE_URL`

---

### Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-username/fastapi-bank-api.git
cd fastapi-bank-api
cd fast_api_test
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```
4. **Create a .env file in the root directory and set your DATABASE_URL** 
DATABASE_URL=postgresql://username:password@localhost:5432/testdb

5. **Running the Server**
```bash
uvicorn app.main:app --reload
```
Navigate to http://localhost:8000 to access the root endpoint.

Interactive Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

---
## API Endpoints

### Account
**POST /accounts/ – Create an account**
**PUT /accounts/{account_id} – Update account**

### Transaction
**POST /transactions/ – Deposit or withdraw**

**GET /transactions/{account_id}?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD – Get transaction history**

---