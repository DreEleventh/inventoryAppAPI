from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

import app.schemas as schemas
import app.models as models
from app.databaseConnection import get_db

financial_router = APIRouter(
    prefix="/financial",
    tags=['Financial Quarter']
)


@financial_router.post("/add_quarter", status_code=status.HTTP_201_CREATED, response_model=schemas.FinancialQuartersResponse)
async def add_quarter(quarter_data: schemas.AddFinancialQuarters, db: Session = Depends(get_db)):
    """End point for adding a new financial quarter

    Args:
        quarter_data (schemas.AddFinancialQuarters): Contains data based to the end point and validated by the relivant schema
        db (Session, optional): Database connection. Defaults to Depends(get_db).

    Returns:
        json: json representation of the entered quarter
    """
    new_quarter = models.FinancialQuarters(**quarter_data.model_dump())

    db.add(new_quarter)
    db.commit()
    db.refresh(new_quarter)

    return new_quarter

@financial_router.get("/get_quarters", response_model=List[schemas.FinancialQuartersResponse])
async def get_all_quarters(db: Session = Depends(get_db)):
    """Endpoint for returning all financial quarters from the database

    Args:
        db (Session, optional): Starts a database connection. Defaults to Depends(get_db).

    Returns:
        dict: a dictionary representation of the financial quarter data
    """
    quarters = db.query(models.FinancialQuarters).order_by(models.FinancialQuarters.id.desc()).all()

    quarters_dict = [quarter.__dict__ for quarter in quarters]

    return quarters_dict


@financial_router.get("/get_quarter_id/{quarter_id}", response_model=schemas.FinancialQuartersResponse)
async def get_quarter_by_id(quarter_id: int, db: Session = Depends(get_db)): 
    """Returns a single financial quarter based on the id provided.

    Args:
        quarter_id (int): A valid financial quarter id
        db (Session, optional): Starts a database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: Rases a 404 HTTP error if no quarter with that id is found.

    Returns:
        json: Returns a json representation of the financial quarter with the id provided.
    """
    quarter = db.query(models.FinancialQuarters).filter(models.FinancialQuarters.id == quarter_id).first()
    
    if quarter is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Financial quarter with id {quarter_id} not fund.")
    
    return quarter
    