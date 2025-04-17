from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, models, database
from fastapi import HTTPException
from typing import List

router = APIRouter()

# @router.post("/", response_model=schemas.CreateTransaction)
@router.post("/", response_model=schemas.TransactionResponse)
def create_transaction(request: schemas.CreateTransaction, db: Session = Depends(database.get_db)):
    account = db.query(models.Account).filter(models.Account.id == request.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if request.transaction_type not in ["deposit", "withdrawal"]:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
    
    if request.transaction_type == "withdrawal":
        if account.balance < request.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        account.balance -= request.amount
    else:
        account.balance += request.amount
    
    new_transaction = models.Transaction(
        account_id=request.account_id,
        amount=request.amount,
        transaction_type=request.transaction_type
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    # return new_transaction
    return {
        "account_id": new_transaction.account_id,
        "amount": new_transaction.amount,
        "transaction_type": new_transaction.transaction_type,
        "balance": account.balance
    }

@router.get("/{account_id}", response_model=List[schemas.ShowTransaction])
def get_transactions(account_id: int, start_date: str, end_date: str, db: Session = Depends(database.get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    transactions = db.query(models.Transaction).filter(
        models.Transaction.account_id == account_id,
        models.Transaction.created_at >= start_date,
        models.Transaction.created_at <= end_date
    ).all()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this account in the given date range")
    
    return transactions
    