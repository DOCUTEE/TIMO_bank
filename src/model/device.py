from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base
from .association import customer_device

class Device(Base):
    __tablename__ = "device"

    device_id = Column(String, primary_key=True)
    device_type = Column(String)
    os = Column(String)
    is_verified = Column(Boolean)
    first_seen = Column(String)
    last_seen = Column(String)
    app_version = Column(String)
    
    customers = relationship("Customer", secondary=customer_device, back_populates="devices")
    auth_logs = relationship("AuthenticationLog", back_populates="device")
    transactions = relationship("Transaction", back_populates="device")
    risks = relationship("DeviceRisk", back_populates="device")
