from sqlalchemy import and_, select
from src.database.models import Book, Country, book_country_association
from src.database.database import session

# Function to add book only if isbn doesn't exist
def add_book(title, isbn):
    # Check if a book with the given isbn already exists
    book = session.query(Book).filter_by(isbn=isbn).first()

    if not book:
      # If not, create a new book instance and add it to the session
      book = Book(title=title, isbn=isbn)
      session.add(book)

    session.commit()
    return book

def add_country(book, country_code):
    country = session.query(Country).filter_by(country_code = country_code).first()

    # Check if a country with the given code already exists in the table book_country_association
    stmt_country_exists = select(book_country_association.columns.book_id).where(
        and_(
            book_country_association.c.book_id == book.id,
            book_country_association.c.country_id == country.id
        )
    )
    country_exists = session.execute(stmt_country_exists).first()

    if not country_exists:
        # If not, create a new entry in the table book_country_association
        insert_stmt = book_country_association.insert().values(book_id=book.id, country_id=country.id)
        session.execute(insert_stmt)

    session.commit()

def get_countries_by_book(isbn):
    # Get the book id using the isbn
    stmt = (
        select(Country.name)
        .select_from(Book)
        .join(book_country_association, Book.id == book_country_association.c.book_id)
        .join(Country, book_country_association.c.country_id == Country.id)
        .where(Book.isbn == isbn)
    )

    countries = session.execute(stmt).scalars().all()

    return [countries]
