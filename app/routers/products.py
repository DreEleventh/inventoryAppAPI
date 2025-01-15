from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

import app.schemas as schemas
import app.models as models
from app.databaseConnection import get_db

products_router = APIRouter(
    prefix="/products",
    tags=['Products']
)


@products_router.post("/add_products", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductsResponse)
async def add_product(product_data: schemas.AddProducts, db: Session = Depends(get_db)): 
    new_products = models.Products(**product_data.model_dump())
    
    db.add(new_products)
    db.commit()
    db.refresh(new_products)
