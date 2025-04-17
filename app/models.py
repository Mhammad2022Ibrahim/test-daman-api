from sqlalchemy import Integer, String, Float, DateTime, Column, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    email = Column(String(100), nullable = False, unique = True)
    balance = Column(Float, nullable = False, default = 0.0)
    phone = Column(String(20), unique = True)
    address = Column(String(100))
    # created_at = Column(DateTime, default = datetime.utcnow)
    created_at = Column(DateTime, default = datetime.now())
    updated_at = Column(DateTime, default = datetime.now(), onupdate = datetime.now())

    transactions = relationship('Transaction', back_populates = 'account')

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key = True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable = False)
    amount = Column(Float, nullable = False)
    transaction_type = Column(String(20), nullable = False)
    created_at = Column(DateTime, default = datetime.now())
    updated_at = Column(DateTime, default = datetime.now(), onupdate = datetime.now())
    # created_at = Column(DateTime, default = datetime.utcnow)
    # updated_at = Column(DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

    account = relationship('Account', back_populates = 'transactions')