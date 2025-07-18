from sqlalchemy import (
    Column, String, Float, Integer, Boolean, ForeignKey,
    DateTime, Table
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

auth_transaction = Table(
    "auth_transaction",
    Base.metadata,
    Column("transaction_id", String, ForeignKey("transaction.transaction_id"), primary_key=True),
    Column("auth_log_id", String, ForeignKey("authentication_log.auth_log_id"), primary_key=True)
)

customer_device = Table(
    "customer_device",
    Base.metadata,
    Column("customer_id", String, ForeignKey("customer.customer_id"), primary_key=True),
    Column("device_id", String, ForeignKey("device.device_id"), primary_key=True)
)

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(String, primary_key=True)
    full_name = Column(String)
    date_of_birth = Column(String)
    email = Column(String)
    customer_pwd = Column(String)
    phone_number = Column(String)
    identity_type = Column(String)
    identity_number = Column(String)
    created_at = Column(String)

    accounts = relationship("Account", back_populates="customer")
    devices = relationship("Device", secondary=customer_device, back_populates="customers")
    risks = relationship("CustomerRisk", back_populates="customer")
    auth_logs = relationship("AuthenticationLog", back_populates="customer")


class Account(Base):
    __tablename__ = "account"
    account_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customer.customer_id"))
    account_number = Column(String)
    account_type = Column(String)
    balance = Column(Float)
    acc_status = Column(String)
    date_opened = Column(String)
    date_closed = Column(String)

    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Device(Base):
    __tablename__ = "device"

    device_id = Column(String, primary_key=True)
    device_type = Column(String)
    os = Column(String)
    is_verified = Column(Boolean)
    first_seen = Column(String)
    last_seen = Column(String)
    app_version = Column(String)
    device_fingerprint = Column(String)

    customers = relationship("Customer", secondary=customer_device, back_populates="devices")
    transactions = relationship("Transaction", back_populates="device")
    risks = relationship("DeviceRisk", back_populates="device")
    auth_logs = relationship("AuthenticationLog", back_populates="device")

class Transaction(Base):
    __tablename__ = "transaction"
    transaction_id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("account.account_id"))
    device_id = Column(String, ForeignKey("device.device_id"))
    amount = Column(Float)
    transaction_type = Column(String)
    transaction_time = Column(String)
    description = Column(String)

    account = relationship("Account", back_populates="transactions")
    device = relationship("Device", back_populates="transactions")
    risks = relationship("TransactionRisk", back_populates="transaction")
    auth_logs = relationship("AuthenticationLog", secondary=auth_transaction, back_populates="transactions")

