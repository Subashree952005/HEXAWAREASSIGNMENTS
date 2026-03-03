from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.services.product_service import ProductService
print("PRODUCT CONTROLLER LOADED")
router = APIRouter(
    prefix="/products",
    tags=["Products"]   # <-- THIS IS IMPORTANT
)

@router.post("/", response_model=ProductResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return ProductService.create_product(db, data)

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return ProductService.get_all_products(db)