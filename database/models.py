# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  November 03, 2024 15:34:21
# Database: sqlite:////tmp/tmp.Kv6bhKmrvC/test/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Customer(SAFRSBaseX, Base):
    """
    description: Represents customers of the test app.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    balance = Column(Float)
    credit_limit = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")



class Product(SAFRSBaseX, Base):
    """
    description: Represents products available for sale.
    """
    __tablename__ = 'products'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductSupplierList : Mapped[List["ProductSupplier"]] = relationship(back_populates="product")
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="product")



class Supplier(SAFRSBaseX, Base):
    """
    description: Represents suppliers of products.
    """
    __tablename__ = 'suppliers'
    _s_collection_name = 'Supplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductSupplierList : Mapped[List["ProductSupplier"]] = relationship(back_populates="supplier")



class Order(SAFRSBaseX, Base):
    """
    description: Represents orders placed by customers.
    """
    __tablename__ = 'orders'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime)
    amount_total = Column(Float)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="order")



class ProductSupplier(SAFRSBaseX, Base):
    """
    description: Link table representing product suppliers.
    """
    __tablename__ = 'product_suppliers'
    _s_collection_name = 'ProductSupplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    supplier_id = Column(ForeignKey('suppliers.id'), nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("ProductSupplierList"))
    supplier : Mapped["Supplier"] = relationship(back_populates=("ProductSupplierList"))

    # child relationships (access children)



class OrderItem(SAFRSBaseX, Base):
    """
    description: Represents items in each order.
    """
    __tablename__ = 'order_items'
    _s_collection_name = 'OrderItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderItemList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderItemList"))

    # child relationships (access children)
