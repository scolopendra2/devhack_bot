import sqlalchemy
from sqlalchemy.orm import relationship
from .users import Employee, Resident

from loader import Base


class Parking(Base):
    __tablename__ = 'parkings'

    id = sqlalchemy.Column(
        sqlalchemy.BigInteger, primary_key=True, autoincrement=True
    )
    number_place = sqlalchemy.Column(sqlalchemy.Integer)
    is_busy = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=0)

    employee = relationship('Employee', back_populates='parking')
    resident = relationship('Resident', back_populates='parking')
