from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Product Category Model
class ProductCategory(Base):
    __tablename__ = 'product_categories'

    id = Column(Integer, primary_key=True, index=True)
    category_description = Column(String, index=True)

    products = relationship("Product", back_populates="category")
    def to_dict(self):
        return {"id": self.id, "category_description": self.category_description}

# Product Model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    product_description = Column(String, index=True)
    product_category = Column(Integer, ForeignKey('product_categories.id'))

    category = relationship("ProductCategory", back_populates="products")
    stock = relationship("ProductStock", back_populates="product")
    def to_dict(self):
        return {"id": self.id, "product_description": self.product_description, "product_category": self.product_category}
# Product Stock Model
class ProductStock(Base):
    __tablename__ = 'product_stock'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    measurement_unit = Column(String)

    product = relationship("Product", back_populates="stock")
    def to_dict(self):
        return {"id": self.id, "product_id": self.product_id, "quantity": self.quantity, "measurement_unit": self.measurement_unit}
