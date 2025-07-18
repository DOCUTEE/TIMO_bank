from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import BigInteger

class Account(Base):
    __tablename__ = "account"

    account_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customer.customer_id"))
    account_number = Column(String)
    account_type = Column(String)
    balance = Column(BigInteger)
    acc_status = Column(String)
    date_opened = Column(String)
    date_closed = Column(String)

    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
