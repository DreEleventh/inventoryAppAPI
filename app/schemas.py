from ast import pattern
from pydantic import BaseModel, EmailStr, ValidationError, field_validator
from datetime import datetime
from typing import Any, Optional, List
from enum import Enum
import re


#----------------------- Financial Quarter Schemas -----------------------
class FinancialQuartersBase(BaseModel):
    """Base schema for financial quarters, used for validation and shared attributes.

    Args:
        BaseModel (base schema): The pydantic base model all other models inherit from
    """
    year: int
    start_date: datetime
    end_date: datetime
    description: Optional[str] = None

class AddFinancialQuarters(FinancialQuartersBase):
    """Schema for adding a new financial quarter to the database

    Args:
        FinancialQuartersBase (pydantic class): The base schema containing shared attributes
    """
    pass

class FinancialQuartersResponse(FinancialQuartersBase):
    """Schema for API responses related to financial quarters.

    Args:
        FinancialQuartersBase (Pydantic schema): The base class this current class inherits from
    """
    id: int
    date_created: datetime
    
     # Indicates that the schema should populate its fields from ORM model attributes.
    class Config:
        form_attribute = True

#----------------------- Products Schemas -----------------------
class ProductCategoryBase(BaseModel):
    """Base schema for validating product category data.

    Args:
        BaseModel (base schema): The base class from which all pydantic classes inherit from
    """
    code: str
    category: str
    description: Optional[str] = None

class AddProductCategory(ProductCategoryBase):
    """Schema for adding a new product category to the database.

    Args:
        ProductCategoryBase (pydantic schema): The base schema containing shared attributes.
    """
    pass

class ProductCategoryResponse(ProductCategoryBase):
    """Schema for API response related to product categories

    Args:
        ProductCategoryBase (pydantic): The Base schema containing shared 
        attributes for product categories
    """
    id: int
    date_created: datetime
    date_updated: Optional[datetime]
    
    # Indicates that the schema should populate its fields from ORM model attributes.
    class Config: 
       from_attributes = True

class BarcodeType(str, Enum): 
    upc = "UPC"
    ean_13 = "EAN-13"
    ean_8 = "EAN-8"
    code_128 = "Code128"
    qr_code = "QRCode"
    itf_14 = "ITF-14"
    code_39 = "Code29"

class ProductsBase(BaseModel):
    """Base schema for validating product-related data

    Args:
        BaseModel (pydantic schema): The pydantic base model all other models inherit from
    """
    product_code: str
    product_name: str
    barcode: str
    barcode_type: BarcodeType
    description: str
    category_id: int
    selling_price: float
    stock_count: int
    reorder_level: int
    financial_quarter_id: int
    
    # Validation patterns for each barcode type
    VALIDATION_PATTERNS = {
        BarcodeType.upc: r'^\d{12}$',
        BarcodeType.ean_13: r'^\d{13}', 
        BarcodeType.ean_8: r'^\d{8}', 
        BarcodeType.code_128: r'^[\x00-\x7F]+$',
        BarcodeType.qr_code: r'^[\x00-\xFF]+$', 
        BarcodeType.itf_14: r'^\d{14}$',
        BarcodeType.code_39: r'^[A-Z0-9\-\.\$\/\+\%\s]+$'
    }
    
    ERROR_MESSAGES ={
        BarcodeType.upc: "UPC must be exactly 12 digits", 
        BarcodeType.ean_13: "EAN-13 must be exactly 13 digits", 
        BarcodeType.ean_8: "EAN-8 must be exactly 8 digits", 
        BarcodeType.code_128: "Code128 must contain only ASCII characters", 
        BarcodeType.qr_code: "QR Code can contain any character",
        BarcodeType.itf_14: "ITF-14 must be exactly 14 digits", 
        BarcodeType.code_39: "Code39 must contain only uppercase letters, numbers, and special characters (- . $ / + %)"
    }
    
    # Field validator for 'barcode'    
    @field_validator('barcode', mode="before")
    def validate_barcode(cls, value: str) -> str:
        """Strip whitespace and validate non-emptiness of barcode."""
        if not isinstance(value, str) or not value.strip(): 
            raise ValueError("barcode cannot be empty or non-string")
        return value.strip()
    
    @field_validator("barcode", mode="after")
    def validate_barcode_with_type(cls, value: str, values: dict[str, Any]) -> str:
        """Validate the barcode based on its type."""
        barcode_type = values.get("barcode_type")
        if not barcode_type:
            raise ValueError("Barcode type is required for validation.")
        
        pattern = cls.VALIDATION_PATTERNS.get(barcode_type)
        if not pattern or not re.fullmatch(pattern, value):
            raise ValueError(cls.ERROR_MESSAGES.get(barcode_type, "Invalid barcode format"))
        
        # Check digit validation for applicable types
        if barcode_type in {BarcodeType.upc, BarcodeType.ean_13, BarcodeType.ean_8}:
            if not cls._validate_check_digit(value, barcode_type): 
                raise ValueError(f"Invalid check digit for {barcode_type.value}")
            
        return value
    
    @staticmethod
    def _validate_check_digit(barcode: str, barcode_type: BarcodeType) -> bool:
        """Validates the check for UPC, EAN-13, AND EAN-8 barcodes."""
        def calculate_check_digit(digits: str) -> int:
            total = 0 
            for i, digit in enumerate(digits[:-1]):
                multiplier = 3 if i % 2 == (0 if barcode_type == BarcodeType.ean_13 else 1) else 1
                total += int(digit) * multiplier
            return (10 - (total % 10)) % 10 
        
        expected_check = calculate_check_digit(barcode)
        return int(barcode[-1]) == expected_check
    

class AddProducts(ProductsBase):
    """Schema used for adding new product records to the database.

    Args:
        ProductsBase (pydantic schema): The base schema containing shared product attributes.
    """
    pass

class ProductsResponse(ProductsBase):
    """Schema for API responses related to products.

    Args:
        ProductsBase (pydantic model): The base schema containing shared product attributes.
    """
    id: int
    date_added: datetime
    date_modified: Optional[datetime] = None

    class Config:
        form_attribute = True


class DiscountType(str, Enum):
    """Enum representing the types of discounts.

    Args:
        str (str): Ensures Pydantic validates the enum values as strings.
        Enum (Enum): Provides a structured enumeration for allowed discount types.
    """
    percentage = "Percentage"
    fixed_amount = "Fixed Amount"

class ProductDiscountsBase(BaseModel):
    """Base schema for managing product discounts.

    Args:
        BaseModel (pydantic schema): Base schema. 
    """
    product_id: int
    discount_type: DiscountType
    discount_value: float
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool
    description: Optional[str] = None
    updated_at: Optional[datetime]



#----------------------- Employees Schemas -----------------------
class UserGroupBase(BaseModel):
    """Base schema for user group-related data.

    Args:
        BaseModel (pydantic base class): System schema that others inherit from 
    """
    group: str
    description: Optional[str] = None

class AddUserGroup(UserGroupBase):
    """Schema used for adding new user groups.

    Args:
        UserGroupBase (pydantic schema): The base schema containing shared user group attributes.
    """
    pass

class UserGroupResponse(BaseModel):
    """Schema for API responses related to user groups.

    Args:
        BaseModel (pydantic schema): System schema that others inherit from.
    """
    id: int
    group: str
    date_created: datetime

    class Config:
        form_attributes = True

