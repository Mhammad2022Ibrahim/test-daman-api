from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database
from fastapi import HTTPException

router = APIRouter()

@router.post("/", response_model=schemas.AccountResponse)
def create_account(request: schemas.CreateAccount, db: Session = Depends(database.get_db)):

    existing_account = db.query(models.Account).filter(models.Account.email == request.email).first()
    if existing_account:
        raise HTTPException(status_code=400, detail="Account with this email already exists")
    else:
        new_account = models.Account(
            name=request.name,
            email=request.email,
            balance=request.balance,
            phone=request.phone,
            address=request.address
        )
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        # return new_account
        return {
            "id": new_account.id,
            "name": new_account.name,
            "balance": new_account.balance,
            "message": f"Account created successfully for {new_account.name}"
        }

@router.put("/{account_id}", response_model=schemas.UpdateAccount)
def update_account(account_id: int, request: schemas.UpdateAccount, db: Session = Depends(database.get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Update only the non-None fields from the request
    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(account, key, value)

    db.commit()
    db.refresh(account)
    return account
