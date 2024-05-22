from lxml import etree
from src.onix_parser.query_utils import add_countries, add_book, get_countries_by_book
from itertools import product
import logging

logging.basicConfig(level=logging.ERROR)

def generate_combinations(word_list, words_to_keep = None):
    combinations = set()
    # Apply transformations to each word in the list and collect results
    for word in word_list:
        combinations.update({word.lower(), word.upper(), word.capitalize()})

    # Add the words to keep as is to the set
    if words_to_keep is not None:
        combinations.update(words_to_keep)

    return list(combinations)

# Tag mappings for normal and short tags
tag_mappings = {
    'Product': generate_combinations(['product']), #['Product', 'product']
    'TitleText': generate_combinations(['TitleText', 'b203'], ['TitleText']), #['TitleText', 'b203']
    'SalesRights': generate_combinations(['salesrights'], ['SalesRights']), #['SalesRights', 'salesrights']
    'RightsCountry': generate_combinations(['CountriesIncluded', 'x449'], ['CountriesIncluded']), #['CountriesIncluded', 'x449']
    'ProductIdentifier': generate_combinations(['productidentifier'], ['ProductIdentifier']), #['ProductIdentifier', 'productidentifier']
    'ProductIDType': generate_combinations(['ProductIDType', 'b221'], ['ProductIDType']), #['ProductIDType', 'b221']
    'ISBN': generate_combinations(['IDValue', 'b244'], ['IDValue']), #['IDValue', 'b244']
}

def get_tag_combinations(tag_array_1, tag_array_2):
    combinations = list(product(tag_mappings[tag_array_1], tag_mappings[tag_array_2]))

    xpath_parts = [f'//{tag_1}//{tag_2}' for tag_1, tag_2 in combinations]

    # Join the parts with the | operator to create the final XPath expression
    xpath_query = '|'.join(xpath_parts)

    return xpath_query

def extract_isbn(product):
    isbn_product_id_type = '15'
    try:
        # Find the ProductIdentifier elements
        for product_identifier in product.xpath('.//{}'.format('|.//'.join(tag_mappings['ProductIdentifier']))):

            product_id_type = product_identifier.xpath('.//{}'.format('|.//'.join(tag_mappings['ProductIDType'])))
            id_value = product_identifier.xpath('.//{}'.format('|.//'.join(tag_mappings['ISBN'])))

            if product_id_type and id_value and product_id_type[0].text == isbn_product_id_type:
                isbn = id_value[0].text
                return isbn

        raise ValueError("ISBN not found in the provided ONIX file.")

    except etree.XMLSyntaxError as e:
        logging.error(f"XML syntax error: {e.msg}")
    except Exception as e:
        logging.error(f"Unexpected error: {e.args[0]}")

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

            countries_xpath = get_tag_combinations('SalesRights', 'RightsCountry')
            countriesList = product.xpath(countries_xpath)

            if len(countriesList) == 0:
                raise ValueError("Missing countries in ONIX data")

            countries = countriesList[0].text.split()
            country_codes = [country_code for country_code in countries]
            add_countries(book, country_codes)

    except etree.XMLSyntaxError as e:
        logging.error(f"XML syntax error: {e.msg}")
    except ValueError as e:
        logging.error(f"Value error: {e.args[0]}")
    except Exception as e:
        logging.error(f"Unexpected error: {e.args[0]}")

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
        logging.error(f"XML syntax error: {e.msg}")
    except ValueError as e:
        logging.error(f"Value error: {e.args[0]}")
    except Exception as e:
        logging.error(f"Unexpected error: {e.args[0]}")

