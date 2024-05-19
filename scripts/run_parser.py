from onix_parser.database import init_db
from onix_parser.parser import parse_onix

if __name__ == "__main__":
    init_db()
    parse_onix('sample_data/2.xml')
