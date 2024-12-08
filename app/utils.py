from sqlalchemy.orm import Session
from sqlalchemy import delete, select
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import ProductCategory, Product, ProductStock
from schemas import ResponseModel, ErrorResponseModel
import logging, os, redis, json
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="{message}", style='{')
redis_host = os.environ.get("REDISHOST")
redis_port = int(os.environ.get("REDISPORT"))
r = redis.StrictRedis(host=redis_host, port=redis_port)
def get_redis():
    return r

def create_response(code=200,status="SUCCESS", details=None):
    try:
        response = ResponseModel(code=code,status=status, details=details)
        json_compatible_item_data = jsonable_encoder(response)
        return JSONResponse(content=json_compatible_item_data)
    except Exception as e:
        logger.exception(f"Exception in create_response >> {e}")
        return JSONResponse(details)
def create_error_response(code=400,status="ERROR", details=None):
    try:
        error = ErrorResponseModel(code=code,status=status, details=details)
        json_compatible_item_data = jsonable_encoder(error)
        return JSONResponse(content=json_compatible_item_data)
    except Exception as e:
        logger.exception(f"Exception in create_response >> {e}")
        return JSONResponse(details)

def get_product_categories(db, skip, limit, redis_key):
    try:
        query = select(ProductCategory).offset(skip).limit(limit)
        result = db.execute(query)
        data_to_return = result.scalars().all()
        json_compatible_data = [item.to_dict() for item in data_to_return]
        # data_to_return = db.query(ProductCategory).offset(skip).limit(limit).all()
        logger.info(f"data_to_return >> {json_compatible_data}")
        try:
            r.set(redis_key, json.dumps(json_compatible_data))
        except:
            r.set(redis_key, json.dumps(str(json_compatible_data)))
        return json_compatible_data
    except Exception as e:
        logger.info(f"Exception trying to get_product_categories >>> {e}")

def create_product_category(db, category):
    try:
        if not category.category_description or category.category_description=="":
            return None
        db_category = ProductCategory(category_description=category.category_description)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        logger.info(f"Product category added!")
        return db_category
    except Exception as e:
        logger.info(f"Exception trying to create_product_category >>> {e}")
        return None

def update_product_category(db, category):
    try:
        query = select(ProductCategory).filter_by(id=category.id)
        result = db.execute(query)
        db_category = result.scalars().one_or_none()
        if db_category:
            logger.info(f"db_category >> {db_category}")
            logger.info(f"category.category_description >> {category.category_description}")
            db_category.category_description=category.category_description
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            logger.info(f"Product category updated!")
        return db_category
    except Exception as e:
        logger.info(f"Exception trying to update_product_category >>> {e}")
        return None

def delete_product_category(db, category):
    try:
        query=select(ProductCategory).filter(ProductCategory.category_description==category.category_description)
        result = db.execute(query)
        product_category = result.scalars().one_or_none()
        if product_category:
            db.delete(product_category)
            db.commit()
            logger.info(f"Product category deleted!")
            return True
        return False
    except Exception as e:
        logger.info(f"Exception trying to delete_product_category >>> {e}")
        return False

def get_product(db, skip, limit, redis_key):
    try:
        query = select(Product).offset(skip).limit(limit)
        result = db.execute(query)
        data_to_return = result.scalars().all()
        json_compatible_data = [item.to_dict() for item in data_to_return]
        logger.info(f"data_to_return >> {json_compatible_data}")
        try:
            r.set(redis_key, json.dumps(json_compatible_data))
        except:
            r.set(redis_key, json.dumps(str(json_compatible_data)))
        return json_compatible_data
    except Exception as e:
        logger.info(f"Exception trying to get_products >>> {e}")

def create_product(db, product):
    try:
        if not product.product_description or product.product_description=="":
            return None
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        logger.info(f"Product added!")
        return db_product
    except Exception as e:
        logger.info(f"Exception trying to create_product >>> {e}")
        return None

def update_product(db, product):
    try:
        query = select(Product).filter_by(id=product.id)
        result = db.execute(query)
        db_product = result.scalars().one_or_none()
        if db_product:
            db_product.product_description=product.product_description
            db_product.product_category=product.product_category
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            logger.info(f"Product updated!")
        return db_product
    except Exception as e:
        logger.info(f"Exception trying to update_product >>> {e}")
        return None

def delete_product(db, product):
    try:
        db.delete(Product).filter_by(**product.dict())
        db.commit()
        logger.info(f"Product deleted!")
        return True
    except Exception as e:
        logger.info(f"Exception trying to delete_product >>> {e}")
        return False

def get_product_stock(db, skip, limit, redis_key):
    try:
        query = select(ProductStock).offset(skip).limit(limit)
        result = db.execute(query)
        data_to_return = result.scalars().all()
        json_compatible_data = [item.to_dict() for item in data_to_return]
        logger.info(f"data_to_return >> {json_compatible_data}")
        try:
            r.set(redis_key, json.dumps(json_compatible_data))
        except:
            r.set(redis_key, json.dumps(str(json_compatible_data)))
        return json_compatible_data
    except Exception as e:
        logger.info(f"Exception trying to get_products >>> {e}")
    except Exception as e:
        logger.info(f"Exception trying to get_product_stock >>> {e}")

def create_product_stock(db, stock):
    try:
        db_stock = ProductStock(**stock.dict())
        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
        logger.info(f"Product stock added!")
        return db_stock
    except Exception as e:
        logger.info(f"Exception trying to create_product >>> {e}")

def update_product_stock(db, stock):
    try:
        query = select(ProductStock).filter_by(product_id=stock.product_id)
        result = db.execute(query)
        db_stock = result.scalars().one_or_none()
        if db_stock:
            db_stock.quantity=stock.quantity
            db.add(db_stock)
            db.commit()
            db.refresh(db_stock)
            logger.info(f"Product stock updated!")
        return db_stock
    except Exception as e:
        logger.info(f"Exception trying to update_product_stock >>> {e}")
        return None
    
def delete_product_stock(db, stock):
    try:
        db.delete(ProductStock).filter_by(**stock.dict())
        db.commit()
        logger.info(f"Product stock deleted!")
        return True
    except Exception as e:
        logger.info(f"Exception trying to delete_product_stock >>> {e}")
        return False
    
def get_product_details(db, skip, limit, redis_key):
    try:
        query = (
            db.query(
                Product.product_description,
                ProductCategory.category_description.label("product_category"),
                ProductStock.quantity.label("product_quantity")
            )
            .join(ProductCategory, Product.product_category == ProductCategory.id)
            .join(ProductStock, Product.id == ProductStock.product_id)
            .offset(skip)
            .limit(limit)
        )
        results = query.all()
        data_to_return= [
                {
                    "product_description": result[0],
                    "product_category": result[1],
                    "product_quantity": result[2]
                }
                for result in results
            ]
        try:
            r.set(redis_key, json.dumps(data_to_return))
        except:
            r.set(redis_key, json.dumps(str(data_to_return)))
        return data_to_return
    except Exception as e:
        logger.info(f"Exception trying to get_product_details >>> {e}")
        return []
