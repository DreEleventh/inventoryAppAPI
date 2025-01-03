from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


#----------------------- Financial Quarter Schemas -----------------------
class FinancialQuartersBase(BaseModel):
    year: int
    start_date: datetime
    end_date: datetime
    description: Optional[str] = None

class AddFinancialQuarters(FinancialQuartersBase):
    pass

class FinancialQuartersResponse(FinancialQuartersBase):
    id: int
    date_created: datetime

    class Config:
        form_attribute = True

#----------------------- Products Schemas -----------------------
class ProductCategoryBase(BaseModel):
    code: str
    category: str
    description: Optional[str] = None

class AddProductCategory(ProductCategoryBase):
    pass

class ProductCategoryResponse(ProductCategoryBase):
    id: int
    date_created: datetime
    date_updated: Optional[datetime]

    class Config:
       from_attributes = True


class ProductsBase(BaseModel):
    product_code: str
    product_name: str
    barcode: str
    description: str
    category_id: int
    selling_price: float
    stock_count: int
    financial_quarter_id: int

class AddProducts(ProductsBase):
    pass

class ProductsResponse(ProductsBase):
    id: int
    date_added: datetime
    date_modified: Optional[datetime] = None

    class Config:
        form_attribute = True


class DiscountType(str, Enum):
    percentage = "Percentage"
    fixed_amount = "Fixed Amount"

class ProductDiscountsBase(BaseModel):
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
    group: str
    description: Optional[str] = None

class AddUserGroup(UserGroupBase):
    pass

class UserGroupResponse(BaseModel):
    id: int
    group: str
    date_created: datetime

    class Config:
        form_attributes = True

