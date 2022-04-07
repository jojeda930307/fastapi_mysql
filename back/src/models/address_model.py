from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.config.database import Base, engine
from src.models.user_model import UserModel


class AddressModel(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    city = Column(String(255))
    location = Column(String(255))
    street = Column(String(255))
    flat = Column(String(255))
    door = Column(String(255))
    postal_code = Column(String(255))
    user_id = Column(Integer, ForeignKey(UserModel.id, ondelete='CASCADE'))

    user_address = relationship("UserModel", back_populates="address_")


Base.metadata.create_all(engine)
