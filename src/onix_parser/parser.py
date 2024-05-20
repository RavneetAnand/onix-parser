from lxml import etree
from src.onix_parser.query_utils import add_country, add_book, get_countries_by_book
import logging

logging.basicConfig(level=logging.ERROR)

# Tag mappings for normal and short tags
tag_mappings = {
    'Product': ['Product', 'product'],
    'TitleText': ['TitleText', 'b203'],
    'SalesRights': ['SalesRights', 'salesrights'],
    'RightsCountry': ['CountriesIncluded', 'x449'],
    'ProductIdentifier': ['ProductIdentifier', 'productidentifier'],
    'ProductIDType': ['ProductIDType', 'b221'],
    'ISBN': ['IDValue', 'b244'],
}

def extract_isbn(product):
    try:
        # Find the ProductIdentifier elements
        for product_identifier in product.xpath('.//{}'.format('|.//'.join(tag_mappings['ProductIdentifier']))):

            product_id_type = product_identifier.xpath('.//{}'.format('|.//'.join(tag_mappings['ProductIDType'])))
            id_value = product_identifier.xpath('.//{}'.format('|.//'.join(tag_mappings['ISBN'])))

            if product_id_type and id_value and product_id_type[0].text == '15':
                isbn = id_value[0].text
                return isbn

        raise ValueError("ISBN not found in the provided ONIX file.")
    except etree.XMLSyntaxError as e:
        logging.error("XML syntax error: ", e)

    except Exception as e:
        logging.error("Unexpected error: ", e)

def parse_onix(file_path):
    try:
        tree = etree.parse(file_path)
        if tree is None:
            raise ValueError("No data found in ONIX file")

        product_xpath = '{}'.format('|'.join(tag_mappings['Product']))

        for product in tree.xpath(product_xpath):
            titleList = product.xpath('.//{}'.format('|.//'.join(tag_mappings['TitleText'])))
            if titleList is None:
                raise ValueError("Missing title in ONIX data")

            if len(titleList) > 1:
                raise ValueError("Multiple titles found in ONIX data")

            title = titleList[0].text
            isbn = extract_isbn(product)

            book = add_book(title, isbn)

            sales_rights = product.xpath('.//{}'.format('|.//'.join(tag_mappings['SalesRights'])))
            if sales_rights is None:
                raise ValueError("Missing sales right information in ONIX data")

            for right in sales_rights:
                countriesList = right.xpath('.//{}'.format('|.//'.join(tag_mappings['RightsCountry'])))
                if len(countriesList) == 0:
                    raise ValueError("Missing countries in ONIX data")

                countries = countriesList[0].text.split()

                for country_code in countries:
                    if country_code:
                        add_country(book, country_code)

    except etree.XMLSyntaxError as e:
        logging.error("XML syntax error", e)
    except ValueError as e:
        logging.error("Value error", e)
    except Exception as e:
        logging.error("Unexpected error", e)

def get_book_sales_rights_countries(file_path):
    try:
        tree = etree.parse(file_path)
        if tree is None:
            raise ValueError("No data found in ONIX file")

        product_xpath = '{}'.format('|'.join(tag_mappings['Product']))

        for product in tree.xpath(product_xpath):
            isbn = extract_isbn(product)
            countries = get_countries_by_book(isbn)
            return countries

    except etree.XMLSyntaxError as e:
        logging.error("XML syntax error", e)
    except ValueError as e:
        logging.error("Value error", e)
    except Exception as e:
        logging.error("Unexpected error", e)

