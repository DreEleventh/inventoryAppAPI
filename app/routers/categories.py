# Router for managing product categories

from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

import app.schemas as schemas
import app.models as models
from app.databaseConnection import get_db

category_router = APIRouter(
    prefix="/category",
    tags=['Product Category']
)

@category_router.post("/add_category", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductCategoryResponse)
async def add_category(category_data: schemas.AddProductCategory, db: Session = Depends(get_db)):
    # Check if the category code already exists
    existing_category = db.query(models.ProductCategory).filter(
        models.ProductCategory.code == category_data.code).first()

    if existing_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"A category with code {category_data.code} already exists.")

    new_category = models.ProductCategory(**category_data.model_dump())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@category_router.get("/get_categories", response_model=List[schemas.ProductCategoryResponse])
async def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(models.ProductCategory).order_by(models.ProductCategory.id.desc()).all()

    category_dict = [category.__dict__ for category in categories]

    return category_dict


@category_router.get("/get_category_by_id/{category_id}", response_model=schemas.ProductCategoryResponse)
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):

    category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with ID {category_id} not found.")

    return category


@category_router.get("/get_category_by_code/{category_code}", response_model=schemas.ProductCategoryResponse)
async def get_category_by_code(category_code: str, db: Session = Depends(get_db)):

    category = db.query(models.ProductCategory).filter(models.ProductCategory.code == category_code).first()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with code {category_code} not found.")

    return category


@category_router.put("/update_category/{category_id}")
async def update_category(category_id: int, category_update: schemas.AddProductCategory, db: Session = Depends(get_db)):
    update_category_query = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id)

    categoty = update_category_query.first()

    if categoty is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {category_id} not found.")

    update_category_query.update(category_update.dict(), synchronize_session=False)
    db.commit()

    return update_category_query.first()

