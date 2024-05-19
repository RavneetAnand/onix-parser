import os
from fastapi import FastAPI, HTTPException
from onix_parser.database import init_db
from onix_parser.parser import parse_onix

app = FastAPI()

# SQLAlchemy setup
init_db()

@app.post("/uploadfile/")
async def upload_file(file_name: str):
  sample_data_path = 'sample_data'
  file_name = file_name + '.xml'
  file_path = os.path.join(sample_data_path, file_name)

  if not os.path.isfile(file_path):
      raise HTTPException(status_code=404, detail="File not found")

  print(f"Processing file: {file_path}")
  # Call the parse_onix function
  parse_onix(file_path)