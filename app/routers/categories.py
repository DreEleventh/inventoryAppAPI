"""
Router for managing product categories
"""

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
    """End point for adding a new product category

    Args:
        category_data (schemas.AddProductCategory): Stores product category data provided by the user
        db (Session, optional): Starts a database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: Returns a 409 error is the category code already exist.

    Returns:
        json: Returns a json representation of the category entered
    """
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
    """Returns all product categories

    Args:
        db (Session, optional): Stores a database connection. Defaults to Depends(get_db).

    Returns:
        dict: Returns a json representation of all product categories stored in a python dictionary
    """
    categories = db.query(models.ProductCategory).order_by(models.ProductCategory.id.desc()).all()

    category_dict = [category.__dict__ for category in categories]

    return category_dict


@category_router.get("/get_category_by_id/{category_id}", response_model=schemas.ProductCategoryResponse)
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """End point that returns a single product category based on the id provided

    Args:
        category_id (int): ID associated with a product category
        db (Session, optional): Stores the instance of a database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: Rases a HTTP error if the id provided does not correspond to any category

    Returns:
        json: json representation of the corresponding product category
    """
    category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with ID {category_id} not found.")

    return category


@category_router.get("/get_category_by_code/{category_code}", response_model=schemas.ProductCategoryResponse)
async def get_category_by_code(category_code: str, db: Session = Depends(get_db)):
    """Returns a single product category based on the category code provided

    Args:
        category_code (str): Code associated with a category
        db (Session, optional): Stores a database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: Rases an HTTP error is not category corresponds with the code provided

    Returns:
        json: Returns a json representation of a category 
    """
    category = db.query(models.ProductCategory).filter(models.ProductCategory.code == category_code).first()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with code {category_code} not found.")

    return category


@category_router.put("/update_category/{category_id}")
async def update_category(category_id: int, category_update: schemas.AddProductCategory, db: Session = Depends(get_db)):
    """End point used to update a product category depending on the id provided 

    Args:
        category_id (int): A category id
        category_update (schemas.AddProductCategory): Stores and validates the data to be updated
        db (Session, optional): Stores a database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: Rases a HTTP error of the id provided does not match any product category

    Returns:
        json: Returns a json representation of the updated product category
    """
    update_category_query = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id)

    category = update_category_query.first()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {category_id} not found.")

    update_category_query.update(category_update.dict(), synchronize_session=False)
    db.commit()

    return update_category_query.first()

