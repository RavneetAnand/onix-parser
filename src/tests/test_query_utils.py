import unittest
from unittest.mock import patch, MagicMock
from database.models import Book
from onix_parser.query_utils import add_book

class TestAddBookFunction(unittest.TestCase):

    # Test the add_book function with a new title for an existing book
    @patch('database.database.session')
    def test_add_book_already_exists(self, mock_session):
        # Mock the existing book in the database
        existing_book = Book(title="Demo", isbn="19785555555557")
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = existing_book
        mock_session.query.return_value = mock_query

        # Call the function
        book = add_book("New title", "9785555555557")

        # Verify that the book returned is the existing one
        self.assertEqual(book.title, "Demo")
        self.assertEqual(book.isbn, "9785555555557")
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

if __name__ == '__main__':
    unittest.main()
