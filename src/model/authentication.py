from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class AuthenticationMethod(Base):
    __tablename__ = "authentication"

    auth_method = Column(String, primary_key=True)
    is_strong = Column(Boolean)
    
class AuthenticationLog(Base):
    __tablename__ = "authentication_log"

    auth_log_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customer.customer_id"))
    device_id = Column(String, ForeignKey("device.device_id"))
    auth_method = Column(String, ForeignKey("authentication.auth_method"))
    auth_time = Column(String)
    status = Column(String)
    used_for = Column(String)

    customer = relationship("Customer", back_populates="auth_logs")
    device = relationship("Device", back_populates="auth_logs")
    method = relationship("AuthenticationMethod")
    transactions = relationship("AuthTransaction", back_populates="auth_log")

class AuthTransaction(Base):
    __tablename__ = "auth_transaction"

    transaction_id = Column(String, ForeignKey("transaction.transaction_id"), primary_key=True)
    auth_log_id = Column(String, ForeignKey("authentication_log.auth_log_id"), primary_key=True)

    transaction = relationship("Transaction", back_populates="auth_logs")
    auth_log = relationship("AuthenticationLog", back_populates="transactions")
