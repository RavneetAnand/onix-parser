import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.database.database import init_db
from src.onix_parser.parser import get_book_sales_rights_countries, parse_onix

app = FastAPI()

# SQLAlchemy setup
init_db()

def validate_file_name(file_name: str):
  if not file_name.strip():
      raise HTTPException(status_code=400, detail="File name is required")

  sample_data_path = 'sample_data'
  file_name = file_name + '.xml'
  file_path = os.path.join(sample_data_path, file_name)

  if not os.path.isfile(file_path):
      raise HTTPException(status_code=404, detail="File not found")

  return file_path

class ParseResponse(BaseModel):
    status: str

@app.post("/parse/")
async def parse_file(file_name: str) -> ParseResponse:
  """
    Parse the ONIX file and upload the countries where the book can be sold.

    - **file_name**: The ONIX file to be parsed.
    """
  file_path = validate_file_name(file_name)

  try:
      parse_onix(file_path)
      return ParseResponse(status="file parsed successfully")
  except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

class CountriesResponse(BaseModel):
    countries: List[str]

@app.get("/getcountries/{file_name}", response_model=CountriesResponse)
async def getcountries(file_name: str):
    """
    Get the countries where the book can be sold.

    - **file_name**: The name of the book's ONIX file.
    """
    file_path = validate_file_name(file_name)

    countries = get_book_sales_rights_countries(file_path)

    return CountriesResponse(countries=countries)
