import sqlalchemy
from sqlalchemy.orm import relationship
import bcrypt

from loader import Base


class AbstractUser(Base):
    __abstract__ = True

    id = sqlalchemy.Column(
        sqlalchemy.BigInteger, primary_key=True, autoincrement=True
    )
    tg_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    surname = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    patronymic = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    phone_number = sqlalchemy.Column(sqlalchemy.VARCHAR(255))


class Employee(AbstractUser):
    __tablename__ = 'employees'

    login = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    password_hash = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    is_admin = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    apartment_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey('appartaments.id')
    )
    parking_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey('parkings.id')
    )

    cars = relationship('Car', back_populates='employee')
    appartament = relationship('Appartament', back_populates='employee')
    parking = relationship('Parking', back_populates='employee')

    def set_password(self, password):
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        )
        self.password_hash = hashed_password.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'), self.password_hash.encode('utf-8')
        )


class Resident(AbstractUser):
    __tablename__ = 'residents'

    apartment_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey('appartaments.id')
    )
    parking_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey('parkings.id')
    )

    cars = relationship('Car', back_populates='resident')
    appartament = relationship('Appartament', back_populates='resident')
    parking = relationship('Parking', back_populates='resident')
