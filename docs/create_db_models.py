# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Customer(Base):
    """description: Represents customers of the test app."""
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    credit_limit = Column(Float, default=500.0)

class Product(Base):
    """description: Represents products available for sale."""
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)

class Order(Base):
    """description: Represents orders placed by customers."""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    amount_total = Column(Float, default=0.0)

class OrderItem(Base):
    """description: Represents items in each order."""
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

class Supplier(Base):
    """description: Represents suppliers of products."""
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)

class ProductSupplier(Base):
    """description: Link table representing product suppliers."""
    __tablename__ = 'product_suppliers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)

# Creating the database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Creating sample data
customer1 = Customer(name="Alice Johnson", email="alice@example.com", balance=150.0, credit_limit=300.0)
customer2 = Customer(name="Bob Smith", email="bob@example.com", balance=50.0, credit_limit=200.0)

product1 = Product(name="Gadget-X", price=99.99, description="A high-tech gadget.")
product2 = Product(name="Tool-Y", price=29.99, description="A useful tool for everyday tasks.")

supplier1 = Supplier(name="Tech Suppliers Inc", contact_info="techsupp@example.com")
supplier2 = Supplier(name="Tool Suppliers Ltd", contact_info="toolsupp@example.com")

order1 = Order(customer_id=1, order_date=datetime.datetime(2023, 10, 4), amount_total=199.98)
order2 = Order(customer_id=2, order_date=datetime.datetime(2023, 11, 15), amount_total=29.99)

order_item1 = OrderItem(order_id=1, product_id=1, quantity=2, amount=199.98)

product_supplier1 = ProductSupplier(product_id=1, supplier_id=1)
product_supplier2 = ProductSupplier(product_id=2, supplier_id=2)

session.add_all([customer1, customer2, product1, product2, supplier1, supplier2, order1, order2, order_item1, product_supplier1, product_supplier2])
session.commit()

# Adding additional rows to satisfy 24-row requirement
for i in range(3, 13):
    session.add(Customer(name=f"Customer {i}", email=f"cust{i}@example.com", balance=100.0))

for i in range(3, 8):
    session.add(Product(name=f"Product-{i}", price=10.0 * i, description=f"Product description {i}"))

# Adding more instances of orders and items
session.add(Order(customer_id=1, order_date=datetime.datetime(2022, 6, 1), amount_total=59.99))
session.add(OrderItem(order_id=2, product_id=1, quantity=1, amount=99.99))

session.commit()

session.close()
