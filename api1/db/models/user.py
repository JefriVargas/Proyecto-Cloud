from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    PrimaryKeyConstraint,
    ForeignKeyConstraint
)

from ..db_setup import Base

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('id'),
    )

    user_data = relationship(
        'UserData',
        back_populates='user',
        cascade='all, delete'
    )

class UserData(Base):
    __tablename__ = 'user_data'

    user_id = Column(Integer)
    names = Column(String(50), nullable=False)
    lastnames = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    age = Column(Integer, nullable=False)
    birthday = Column(Date, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id'),
        ForeignKeyConstraint(['user_id'], ['users.id'])
    )

    user = relationship(
        'User',
        back_populates='user_data'
    )
