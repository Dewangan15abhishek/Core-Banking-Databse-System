from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from db import Base

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)

class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    balance = Column(Float, default=0.0)
    account_type = Column(String, default="savings")

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    from_account = Column(Integer, ForeignKey("accounts.account_id"), nullable=True)
    to_account = Column(Integer, ForeignKey("accounts.account_id"), nullable=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # deposit / withdraw / transfer
    timestamp = Column(DateTime, default=datetime.utcnow)