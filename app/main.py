from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from utils import *
from schemas import *
from models import *
import uvicorn, json

app = FastAPI()

@app.post("/product_categories/")
def create_category(category: ProductCategoryCreate, db: Session = Depends(get_db)):
    try:
        category = create_product_category(db=db, category=category)
        db.close()
        if category is None:
            return create_error_response(details=f"category could not be created!")
        return create_response(details=f"category {category.category_description} created successfully!")
    except Exception as e:
        logger.exception(f"Exception trying to create new category >> {e}!")
        db.close()
        return create_error_response(details=f"Exception trying to create new category!")
    
@app.delete("/product_categories/")
def delete_category(category: ProductCategoryDelete, db: Session = Depends(get_db)):
    try:
        category_deleted = delete_product_category(db=db, category=category)
        db.close()
        if not category_deleted:
            return create_error_response(details=f"category {category.category_description} could not be deleted!")
        return create_response(details=f"category {category.category_description} deleted successfully!")
    except Exception as e:
        logger.exception(f"Exception trying to delete category >> {e}!")
        db.close()
        return create_error_response(details=f"Exception trying to delete category!")
    
@app.patch("/product_categories/")
def update_category(category: ProductCategoryPatch, db: Session = Depends(get_db)):
    try:
        updated_category=update_product_category(db=db, category=category)
        db.close()
        if updated_category is None:
            return create_error_response(details=f"category {category.category_description} could not be updated!")
        return create_response(details=f"category {category.category_description} updated successfully!")
    except Exception as e:
        logger.exception(f"Exception trying to update category >> {e}!")
        db.close()
        return create_error_response(details=f"Exception trying to update category!")

@app.get("/product_categories/")
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),r: redis.StrictRedis = Depends(get_redis)):
    try:
        redis_key = f"product_categories:{skip}-{limit}"
        try:
            product_categories = r.get(redis_key)
        except Exception as e:
            logger.exception(f"Exception trying to get product_categories from redis, {e}")
            product_categories = None
        if product_categories:
            logger.info(f"found in redis")
            db.close()
            return create_response(details=json.loads(product_categories))
        try:
            logger.info(f"searching in db...")
            product_categories=get_product_categories(db=db, skip=skip, limit=limit, redis_key=redis_key)
        except Exception as e:
            logger.exception(f"Exception trying to read_categories, {e}")
            product_categories=None
    except Exception as e:
        logger.exception(f"Exception trying to read_categories, {e}")
        product_categories=None
    db.close()
    if not product_categories:
        return create_error_response(details=f"Product categories could not be retrieved!")
    return create_response(details=product_categories)

@app.post("/products/")
def create_products(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        product = create_product(db=db, product=product)
        db.close()
        if product is None:
            return create_error_response(details=f"product could not be created!")
        return create_response(details=f"product {product.product_description} created successfully!")
    except Exception as e:
        logger.exception(f"Exception trying to create new product >> {e}!")
        db.close()
        return create_error_response(details=f"Exception trying to create new product!")

@app.delete("/products/")
def delete_products(product: ProductDelete, db: Session = Depends(get_db)):
    try:
        product_deleted = delete_product(db=db, product=product)
        db.close()
        if not product_deleted:
            return create_error_response(details=f"product {product.product_description} could not be deleted!")
        return create_response(details=f"product {product.product_description} deleted successfully!")
    except Exception as e:
        logger.exception(f"Exception trying to delete product >> {e}!")
        db.close()
        return create_error_response(details=f"Exception trying to delete product!")

@app.patch("/products/")
def update_products(product: ProductPatch, db: Session = Depends(get_db)):
    try:
        updated_product=update_product(db=db, product=product)
        db.close()
        if updated_product is None:
            return create_error_response(details=f"product {product.product_category} could not be updated!")
        return create_response(details=f"product {product.product_category} updated successfully!")
    except Exception as e:
        logger.exception(f"Exception trying to update product >> {e}!")
        db.close()
        return create_error_response(details=f"Exception trying to update product!")

@app.get("/products/")
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        redis_key = f"products:{skip}-{limit}"
        try:
            products = r.get(redis_key)
        except Exception as e:
            logger.exception(f"Exception trying to get products from redis, {e}")
            products = None
        if products:
            logger.info(f"found in redis")
            db.close()
            return create_response(details=json.loads(products))
        try:
            logger.info(f"searching in db...")
            products=get_product(db=db, skip=skip, limit=limit, redis_key=redis_key)
        except Exception as e:
            logger.exception(f"Exception trying to read_products, {e}")
            products=None
    except Exception as e:
        logger.exception(f"Exception trying to read_products, {e}")
        products=None
    db.close()
    if not products:
        return create_error_response(details=f"Products could not be retrieved!")
    return create_response(details=products)

@app.post("/product_stock/")
def create_stock(stock: ProductStockCreate, db: Session = Depends(get_db)):
    try:
        product_stock = create_product_stock(db=db, stock=stock)
        db.close()
        if product_stock is None:
            return create_error_response(details=f"product stock could not be created!")
        return create_response(details=f"product stock {product_stock.id} created successfully!")
    except Exception as e:
        logger.exception(f"Exception trying to create new product stock >> {e}!")
        db.close()
        return create_error_response(details=f"Exception trying to create new product stock!")

@app.delete("/product_stock/")
def delete_stock(stock: ProductStockDelete, db: Session = Depends(get_db)):
    try:
        product_stock_deleted = delete_product_stock(db=db, stock=stock)
        db.close()
        if not product_stock_deleted:
            return create_error_response(details=f"product stock {stock.product_id} could not be deleted!")
        return create_response(details=f"product stock {stock.product_id} deleted successfully!")
    except Exception as e:
        logger.exception(f"Exception trying to delete product stock >> {e}!")
        db.close()
        return create_error_response(details=f"Exception trying to delete product stock!")

@app.patch("/product_stock/")
def update_stock(product_stock: ProductStockPatch, db: Session = Depends(get_db)):
    try:
        updated_product_stock=update_product_stock(db=db, product=product_stock)
        db.close()
        if updated_product_stock is None:
            return create_error_response(details=f"product stock {product_stock.product_id} could not be updated!")
        return create_response(details=f"product stock {product_stock.product_id} updated successfully!")
    except Exception as e:
        logger.exception(f"Exception trying to update product stock >> {e}!")
        db.close()
        return create_error_response(details=f"Exception trying to update product stock!")    

@app.get("/product_stock/")
def read_stock(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        redis_key = f"product_stock:{skip}-{limit}"
        try:
            product_stock = r.get(redis_key)
        except Exception as e:
            logger.exception(f"Exception trying to get product stock from redis, {e}")
            product_stock = None
        if product_stock:
            logger.info(f"found in redis")
            db.close()
            return create_response(details=json.loads(product_stock))
        try:
            logger.info(f"searching in db...")
            product_stock=get_product_stock(db=db, skip=skip, limit=limit, redis_key=redis_key)
        except Exception as e:
            logger.exception(f"Exception trying to read_stock, {e}")
            product_stock=None
    except Exception as e:
        logger.exception(f"Exception trying to read_stock, {e}")
        product_stock=None
    db.close()
    if not product_stock:
        return create_error_response(details=f"Product stock could not be retrieved!")
    return create_response(details=product_stock) 

@app.get("/product_details/")
def product_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        redis_key = f"product_details:{skip}-{limit}"
        try:
            product_details = r.get(redis_key)
        except Exception as e:
            logger.exception(f"Exception trying to get product details from redis, {e}")
            product_details = None
        if product_details:
            logger.info(f"found in redis")
            db.close()
            return create_response(details=json.loads(product_details))
        try:
            logger.info(f"searching in db...")
            product_details=get_product_details(db=db, skip=skip, limit=limit, redis_key=redis_key)
        except Exception as e:
            logger.exception(f"Exception trying to get product_details, {e}")
            product_details=None
    except Exception as e:
        logger.exception(f"Exception trying to get product_details, {e}")
        product_details=None
    db.close()
    if not product_details:
        return create_error_response(details=f"Product details could not be retrieved!")
    return create_response(details=product_details) 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)