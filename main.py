import os
from fastapi import FastAPI, HTTPException
from src.database.database import init_db
from src.onix_parser.parser import get_book_sales_rights_countries, parse_onix

app = FastAPI()

# SQLAlchemy setup
init_db()

def validate_file_name(file_name):
  if not file_name:
    raise HTTPException(status_code=400, detail="File name is required")

  sample_data_path = 'sample_data'
  file_name = file_name + '.xml'
  file_path = os.path.join(sample_data_path, file_name)

  if not os.path.isfile(file_path):
      raise HTTPException(status_code=404, detail="File not found")

  return file_path

@app.post("/uploadfile/")
async def upload_file(file_name: str):
  file_path = validate_file_name(file_name)

  parse_onix(file_path)

@app.get("/getcountries/{file_name}")
async def getcountries(file_name: str):
  file_path = validate_file_name(file_name)

  countries = get_book_sales_rights_countries(file_path)

  return {"countries": countries}