import sqlalchemy
from sqlalchemy.orm import relationship
from .users import Employee, Resident

from loader import Base


class Appartament(Base):
    __tablename__ = 'appartaments'

    id = sqlalchemy.Column(
        sqlalchemy.BigInteger, primary_key=True, autoincrement=True
    )
    number_appartament = sqlalchemy.Column(sqlalchemy.Integer)
    padik = sqlalchemy.Column(sqlalchemy.Integer)

    employee = relationship('Employee', back_populates='appartament')
    resident = relationship('Resident', back_populates='appartament')
