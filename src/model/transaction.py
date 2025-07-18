from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("account.account_id"))
    device_id = Column(String, ForeignKey("device.device_id"))
    amount = Column(BigInteger)
    transaction_type = Column(String)
    transaction_time = Column(String)
    description = Column(String)
    status = Column(String)
    account = relationship("Account", back_populates="transactions")
    device = relationship("Device", back_populates="transactions")
    auth_logs = relationship("AuthTransaction", back_populates="transaction")

