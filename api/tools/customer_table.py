from sqlalchemy import Column, String,Float
from tools.base import Base

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(String(250), primary_key=True)
    first_name = Column(String(250))
    last_name = Column(String(250))
    email = Column(String(250))
    gender = Column(String(250))
    country = Column(String(250))
    city = Column(String(250))
    street = Column(String(250))
    phone = Column(String(250))
    total_price = Column(Float)
    currency = Column(String(250))
    credit_card_type = Column(String(250))
    credit_card_number = Column(String(250))

   