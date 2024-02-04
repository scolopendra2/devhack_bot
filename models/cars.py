from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import relationship

from loader import Base


class Car(Base):
    __tablename__ = 'cars'

    id = sqlalchemy.Column(
        sqlalchemy.BigInteger, primary_key=True, autoincrement=True
    )

    gos_number = sqlalchemy.Column(sqlalchemy.TEXT(12))

    date_start = sqlalchemy.Column(sqlalchemy.DATETIME, default=datetime.now())
    date_end = sqlalchemy.Column(sqlalchemy.DATETIME)

    employee_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey('employees.id')
    )
    resident_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey('residents.id')
    )
    employee = relationship('Employee', back_populates='cars')
    resident = relationship('Resident', back_populates='cars')
