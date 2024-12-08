from pydantic import BaseModel
from typing import Optional, Any

# Product Category Schema
class ProductCategoryBase(BaseModel):
    category_description: str

class ProductCategoryCreate(ProductCategoryBase):
    pass
class ProductCategoryDelete(ProductCategoryBase):
    pass
class ProductCategory(ProductCategoryBase):
    id: int
class ProductCategoryPatch(ProductCategoryBase):
    id: int

# Product Schema
class ProductBase(BaseModel):
    product_description: str
    product_category: int

class ProductCreate(ProductBase):
    pass
class ProductDelete(ProductBase):
    pass
class Product(ProductBase):
    id: int
class ProductPatch(ProductBase):
    id: int

# Product Stock Schema
class ProductStockBase(BaseModel):
    product_id: int
    quantity: int
    measurement_unit: str

class ProductStockCreate(ProductStockBase):
    pass
class ProductStockDelete(ProductStockBase):
    pass
class ProductStock(ProductStockBase):
    id: int
class ProductStockPatch(ProductStockBase):
    pass

class ResponseModel(BaseModel):
    code: int
    status: Optional[str] = None
    details: Optional[Any] = None
class ErrorResponseModel(BaseModel):
    code: int
    status: Optional[str] = None
    details: Optional[Any] = None
