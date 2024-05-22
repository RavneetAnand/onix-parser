import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from database.database import populate_countries_table, init_db

class TestDatabaseFunctions(unittest.TestCase):
    @patch('database.database.session')
    @patch('database.database.open', new_callable=mock_open, read_data='{"US": "United States", "CA": "Canada"}')
    def test_populate_countries_table(self, mock_file, mock_session):
        mock_session.query.return_value.first.return_value = None  # Simulate empty table
        mock_country_class = MagicMock()

        with patch('database.database.Country', new=mock_country_class):
            populate_countries_table('ISO3166-1.alpha2.json')

            mock_file.assert_called_once_with('ISO3166-1.alpha2.json', 'r')
            countries_data = json.load(mock_file())
            self.assertEqual(len(countries_data), 2)

            # Check that the session's add_all method was called with the correct arguments
            mock_session.add_all.assert_called_once()
            args, _ = mock_session.add_all.call_args
            added_countries = args[0]

            self.assertEqual(len(added_countries), 2)
            # Check that session.commit was called once
            mock_session.commit.assert_called_once()

    @patch('database.database.populate_countries_table')
    @patch('database.database.engine')
    def test_init_db(self, mock_engine, mock_populate_countries_table):
        mock_base = MagicMock()
        with patch('database.models.Base', new=mock_base):
            init_db()

            mock_base.metadata.create_all.assert_called_once_with(mock_engine)
            mock_populate_countries_table.assert_called_once_with('ISO3166-1.alpha2.json')

if __name__ == '__main__':
    unittest.main()
