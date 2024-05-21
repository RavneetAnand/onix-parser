import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Country
import json
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

logging.basicConfig(level=logging.ERROR)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def populate_countries_table(json_file_path):
    try:
        # Check if the countries table is empty
        if session.query(Country).first() is None:
            with open(json_file_path, 'r') as file:
                countries_data = json.load(file)

            countries = []
            for country_code, name in countries_data.items():
                countries.append(
                    Country(
                        country_code=country_code,
                        name=name
                    )
                )

            session.add_all(countries)
            session.commit()

    except Exception as e:
        session.rollback()
        logging.error("An error occurred", e)

    finally:
        session.close()

def init_db():
    from .models import Base
    Base.metadata.create_all(engine)
    populate_countries_table('ISO3166-1.alpha2.json')
