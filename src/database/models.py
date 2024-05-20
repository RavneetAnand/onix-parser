from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for the many-to-many relationship between Book and Country
book_country_association = Table(
    'book_country', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('country_id', Integer, ForeignKey('countries.id'), primary_key=True)
)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String(13), unique=True, nullable=False)
    title = Column(String(255), nullable=False)

    # Relationship to countries
    countries = relationship(
        'Country', secondary=book_country_association, back_populates='books'
    )

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    # Relationship to books
    books = relationship(
        'Book', secondary=book_country_association, back_populates='countries'
    )

    __table_args__ = (
        UniqueConstraint('country_code', name='uq_country_code'),
    )
