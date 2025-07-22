from sqlalchemy import Table, Column, String, ForeignKey
from .base import Base

customer_device = Table(
    "customer_device",
    Base.metadata,
    Column("customer_id", String, ForeignKey("customer.customer_id"), primary_key=True),
    Column("device_id", String, ForeignKey("device.device_id"), primary_key=True)
)
