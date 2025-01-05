from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


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


class ProductsBase(BaseModel):
    """Base schema for validating product-related data

    Args:
        BaseModel (pydantic schema): The pydantic base model all other models inherit from
    """
    product_code: str
    product_name: str
    barcode: str
    description: str
    category_id: int
    selling_price: float
    stock_count: int
    financial_quarter_id: int

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
    date_modified: Optional[datetime]

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

