from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class CustomerRisk(Base):
    __tablename__ = "customer_risk"

    risk_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customer.customer_id"))
    detected_time = Column(String)
    details = Column(String)

    customer = relationship("Customer", back_populates="risks")

class TransactionRisk(Base):
    __tablename__ = "transaction_risk"

    risk_id = Column(String, primary_key=True)
    transaction_id = Column(String, ForeignKey("transaction_log.transaction_id"))
    detected_time = Column(String)
    details = Column(String)

class DeviceRisk(Base):
    __tablename__ = "device_risk"

    risk_id = Column(String, primary_key=True)
    device_id = Column(String, ForeignKey("device.device_id"))
    detected_time = Column(String)
    details = Column(String)

    device = relationship("Device", back_populates="risks")
