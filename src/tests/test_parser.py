import unittest
from unittest.mock import patch, MagicMock
from onix_parser.parser import parse_onix
from lxml import etree

class TestParseOnix(unittest.TestCase):

    # Test the parse_onix function with a valid file
    @patch('onix_parser.parser.etree.parse')
    @patch('onix_parser.parser.extract_isbn')
    @patch('onix_parser.parser.add_book')
    @patch('onix_parser.parser.get_tag_combinations')
    @patch('onix_parser.parser.add_countries')
    def test_parse_onix_valid(self, mock_add_countries, mock_get_tag_combinations, mock_add_book, mock_extract_isbn, mock_etree_parse):
        valid_file_path = "sample_data/2.xml"
        # Mocking a valid XML structure
        mock_tree = MagicMock()
        mock_product = MagicMock()
        mock_title = MagicMock()

        mock_title.text = "Test Title"

        mock_product.xpath.side_effect = [[mock_title], [MagicMock(text="US")]]
        mock_tree.xpath.return_value = [mock_product]
        mock_etree_parse.return_value = mock_tree

        # Setting mock return values
        mock_add_book.return_value = "Test Title"
        mock_get_tag_combinations.return_value = "//salesrights//x449"

        # Call the parser function
        parse_onix(valid_file_path)

        # Assertions
        mock_etree_parse.assert_called_once_with(valid_file_path)
        mock_add_book.assert_called_once()
        mock_add_countries.assert_called()

    # Test the parse_onix function with a valid file but no title
    @patch('onix_parser.parser.etree.parse')
    def test_parse_onix_missing_title(self, mock_etree_parse):
        valid_file_path = "sample_data/2.xml"
        # Mocking an XML structure with missing title
        mock_tree = MagicMock()
        mock_product = MagicMock()
        mock_product.xpath.side_effect = [None]
        mock_tree.xpath.return_value = [mock_product]

        mock_etree_parse.return_value = mock_tree

        with self.assertLogs(level='ERROR') as log:
            parse_onix(valid_file_path)
            self.assertIn("ERROR:root:Value error: Missing title in ONIX data", log.output)

if __name__ == '__main__':
    unittest.main()
