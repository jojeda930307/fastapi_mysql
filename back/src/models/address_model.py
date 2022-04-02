from sqlalchemy import Column, Integer, String

from src.config.database import Base, engine


class AddressModel(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    city = Column(String(255))
    location = Column(String(255))
    street = Column(String(255))
    flat = Column(String(255))
    door = Column(String(255))
    postal_code = Column(String(255))


Base.metadata.create_all(engine)
