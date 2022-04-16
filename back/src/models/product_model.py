from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.config.database import Base, engine
from src.models.user_model import UserModel


class ProductModel(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    image = Column(String(255))
    description = Column(String(255))
    price = Column(Float)
    user_id = Column(Integer, ForeignKey(UserModel.id, ondelete='CASCADE'))

    order = relationship("UserModel", back_populates="user_order")


Base.metadata.create_all(engine)
