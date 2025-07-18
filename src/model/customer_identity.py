from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class CustomerIdentity(Base):
    __tablename__ = "customer_identity"

    identity_type = Column(String)
    identity_number = Column(String)
    customer_id = Column(String, ForeignKey("customer.customer_id"), unique=True)

    __table_args__ = (
        PrimaryKeyConstraint("identity_type", "identity_number"),
    )

    customer = relationship("Customer", back_populates="identity")
