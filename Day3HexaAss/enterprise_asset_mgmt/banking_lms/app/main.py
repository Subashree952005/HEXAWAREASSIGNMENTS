from fastapi import FastAPI
from app.core.database import Base, engine

from app.controllers.user_controller import router as user_router
from app.controllers.product_controller import router as product_router
from app.controllers.application_controller import router as application_router
from app.controllers.repayment_controller import router as repayment_router

from app.middleware.cors import add_cors
from app.middleware.logging_middleware import log_requests
from app.exceptions.exception_handlers import business_exception_handler
from app.exceptions.custom_exceptions import BusinessException

app = FastAPI()

Base.metadata.create_all(bind=engine)

add_cors(app)
app.middleware("http")(log_requests)

app.add_exception_handler(BusinessException, business_exception_handler)

# ✅ USE NEW ROUTER NAMES HERE
app.include_router(user_router)
app.include_router(product_router)
app.include_router(application_router)
app.include_router(repayment_router)