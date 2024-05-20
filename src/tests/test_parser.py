import pytest
from src.database.database import init_db, session
from src.onix_parser.parser import parse_onix
from src.database.models import Book, Country

@pytest.fixture(scope='module')
def setup_database():
    init_db()
    yield
    session.query(Country).delete()
    session.query(Book).delete()
    session.commit()

def test_parse_onix(setup_database):
    parse_onix('sample_data/1.xml')
    assert session.query(Book).count() == 4
    assert session.query(Country).count() > 0

if __name__ == "__main__":
    pytest.main()
