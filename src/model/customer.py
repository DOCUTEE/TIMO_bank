from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base
from .association import customer_device

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
    auth_logs = relationship("AuthenticationLog", back_populates="customer")
    risks = relationship("CustomerRisk", back_populates="customer")
    identity = relationship("CustomerIdentity", back_populates="customer", uselist=False)
