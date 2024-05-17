from lxml import etree
from .database import session
from .models import Book, Country

def parse_onix(file_path):
    try:
        tree = etree.parse(file_path)
        namespaces = {'onix': 'http://ns.editeur.org/onix/3.0/reference'}

        for product in tree.xpath('//onix:Product', namespaces=namespaces):
            title = product.xpath('string(.//onix:TitleText)', namespaces=namespaces)
            if not title:
                raise ValueError("Missing title in ONIX data")

            book = Book(title=title)
            session.add(book)
            session.commit()

            sales_rights = product.xpath('.//onix:SalesRights', namespaces=namespaces)
            for right in sales_rights:
                countries = right.xpath('.//onix:RightsCountry', namespaces=namespaces)
                for country in countries:
                    country_code = country.text
                    if country_code:
                        country_entry = Country(book_id=book.id, country_code=country_code)
                        session.add(country_entry)
        session.commit()
    except etree.XMLSyntaxError as e:
        print(f"XML syntax error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
