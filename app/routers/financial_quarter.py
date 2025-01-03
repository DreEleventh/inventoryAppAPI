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
    new_quarter = models.FinancialQuarters(**quarter_data.model_dump())

    db.add(new_quarter)
    db.commit()
    db.refresh(new_quarter)

    return new_quarter

@financial_router.get("/get_quarters", response_model=List[schemas.FinancialQuartersResponse])
async def get_all_quarters(db: Session = Depends(get_db)):
    quarters = db.query(models.FinancialQuarters).order_by(models.FinancialQuarters.id.desc()).all()

    quarters_dict = [quarter.__dict__ for quarter in quarters]

    return quarters_dict