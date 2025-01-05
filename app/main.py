# Name of Enterprise App: Inventory System API
# Developers: Andre McKenzie
# Version: 1.0
# Version Date: 2025-01-05
# Purpose: FastAPI backend implementation for a inventory Management system, designed to store use and 
# products data as will as having the ability to generate reports on said data

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.databaseConnection import engine, Base
import app.models
from app.routers import categories, financial_quarter
# Create an async lifespan function
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     Base.metadata.create_all(bind=engine)
#     yield

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.category_router)
app.include_router(financial_quarter.financial_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


