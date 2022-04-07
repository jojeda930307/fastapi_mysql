from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String
from src.config.database import Base, engine


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))

    address_ = relationship("AddressModel",
                            back_populates="user_address",
                            cascade="all, delete",
                            passive_deletes=True)


Base.metadata.create_all(engine)
