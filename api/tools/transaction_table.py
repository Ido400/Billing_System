from sqlalchemy import String, Float, Integer, Column, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from tools.base import Base

class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    user_id_transac = Column(String(250))
    user_id_get = Column(String(250))
    total_before_convert = Column(Float)
    currency_user_transac = Column(String(250))
    total_after_convert = Column(Float)
    currency_user_get = Column(String(250))
    date = Column(DateTime)

  

   