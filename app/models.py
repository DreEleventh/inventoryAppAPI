from datetime import datetime
from sqlalchemy import Boolean, CheckConstraint, Column, Integer, String, Float, ForeignKey, UniqueConstraint, false
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, Text, Enum, DECIMAL, DATE
from enum import Enum as PyEnum

from app.databaseConnection import Base


#==================================== Employees =======================================
class UserGroups(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True, nullable=False)
    group = Column(String(10), unique=True, nullable=False)
    description = Column(String(150), nullable=True)
    date_created = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

class Employees(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, nullable=False)
    employee_id = Column(String(9), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    personal_email = Column(String(50), nullable=True)
    company_email = Column(String(50), nullable=False)
    user_group_id = Column(Integer, ForeignKey("user_groups.id"), nullable=False)
    status = Column(String(1), nullable=False)
    date_created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    user_group = relationship("UserGroups")

class EmployeeCredentials(Base):
    __tablename__ = "employee_credentials"
    id = Column(Integer, primary_key=True, nullable=False)
    employee_id = Column(String(9), ForeignKey('employees.employee_id', ondelete="CASCADE"), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    last_login_time = Column(TIMESTAMP(timezone=True))

    employees = relationship("Employees")
    

#==================================== Products =======================================
class ProductCategory(Base):
    __tablename__ = "product_category"
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String(5), unique=True, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    date_created = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    date_updated = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    products = relationship("Products", back_populates="product_category")

class FinancialQuarters(Base):
    __tablename__ = "financial_quarters"
    id = Column(Integer, primary_key=True, nullable=False)
    year = Column(Integer, nullable=False)
    start_date = Column(TIMESTAMP, default=datetime.now)
    end_date = Column(TIMESTAMP, default=datetime.now)
    description = Column(Text, nullable=True)
    date_created = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    products = relationship("Products", back_populates="financial")

class BarcodeType(PyEnum):
    UPC = "UPC"
    EAN_13 = "EAN-13"
    EAN_8 = "EAN-8"
    CODE_128 = "Code128"
    QR_CODE = "QRCode"

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String(150), nullable=False)
    product_code = Column(String(5), unique=True, nullable=False)
    barcode = Column(String(50), unique=True, nullable=False)
    barcode_type = Column(Enum(BarcodeType), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("product_category.id"), nullable=False)
    selling_price = Column(DECIMAL(19, 4), nullable=False)
    stock_count = Column(Integer, default=0, nullable=False)
    reorder_level = Column(Integer, default=0, nullable=False)
    date_added = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    date_modified = Column(TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=True)
    financial_quarter_id = Column(Integer, ForeignKey("financial_quarters.id"), nullable=False)

    product_category = relationship("ProductCategory", back_populates="products")
    discounts = relationship("ProductDiscounts", back_populates="product")
    financial = relationship("FinancialQuarters", back_populates="products")

    __table_args__=(
        CheckConstraint(
        "barcode_type IN ('UPC', 'EAN-13', 'EAN-8', 'Code128', 'QRCode')", 
        name='check_valid_barcode_type'),
        CheckConstraint(
        "(barcode_type = 'UPC' AND length(barcode) = 12) OR "
        "(barcode_type = 'EAN-13' AND length(barcode) = 13) OR "
        "(barcode_type = 'EAN-8' AND length(barcode) = 8) OR "
        "(barcode_type IN ('Code128', 'QRCode'))", 
        name="check_barcode_length"),
        CheckConstraint('reorder_level <= stock_count', name='check_reorder_level'),
        CheckConstraint('stock_count >= 0', name='check_stock_count_non_negative'),
        CheckConstraint('reorder_level >= 0', name='check_reorder_level_non_negative'),
    )

class ProductDiscounts(Base):
    __tablename__ = "product_discounts"
    id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    discount_type = Column(Enum('Percentage', 'Fixed Amount', name='discount_types'), nullable=False)
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=True)
    is_active = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    product = relationship("Products", back_populates="discounts")

