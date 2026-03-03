import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date, Boolean, Text
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date, Boolean, Text

class AssetType(str, enum.Enum):
    LAPTOP = "LAPTOP"
    MOBILE_DEVICE = "MOBILE_DEVICE"
    MONITOR = "MONITOR"
    SOFTWARE_LICENSE = "SOFTWARE_LICENSE"
    COMPANY_VEHICLE = "COMPANY_VEHICLE"
    OTHER = "OTHER"


class AssetStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    MAINTENANCE = "MAINTENANCE"
    RETIRED = "RETIRED"


class Asset(Base, TimestampMixin):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(50), unique=True, index=True, nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False)
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    purchase_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="AVAILABLE")
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    notes = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)

    department = relationship("Department", back_populates="assets")
    assignments = relationship("AssetAssignment", back_populates="asset")
    maintenance_records = relationship("MaintenanceRecord", back_populates="asset")