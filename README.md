# Onix file parser service

============================

This repository contains the code for a Onix file parser API. The FastAPI service allows for parsing the ebooks ONIX file and upload and fetch the countries where the book can be sold.

This service provides two main endpoints for parsing ONIX 3.0 files and retrieving the countries where books can be sold.

### Endpoints

- `POST /parse/` - Parse and upload to a database an ONIX 3.0 XML file.
- `GET /countries/{file_name}` - Retrieve the countries for a given parsed ONIX file.

## Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- Other dependencies as specified in requirements.txt

## Database

Database used for this app is hosted at AWS MySQL service. App is connecting to it with the help of a connection string.

### Run Using Docker

If you prefer to use Docker to run the service, you can containerize the application using a Dockerfile. Ensure Docker is installed on your machine and build the image using the following command:

```bash
docker build -t onixparserimage .
```

Then, you can run the container:

```bash
docker run -p 3000:3000 onixparserimage
This command will build the Docker image with the tag onixparserservice and run it, exposing the service on port 3000.
```

### Running locally

1. Clone the repository.
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
uvicorn main:app --reload
```

2. Endpoints:

#### Note:

All the details about these endpoints can also be found at this `FastAPI - Swagger UI` link: http://127.0.0.1:8000/docs available after succesfully running the application in step 1.

To interact with the endpoint, you can use any HTTP client like curl, Postman, or write client-side code using frameworks/libraries like Axios, Fetch API, etc.

- POST /parse/

  Upload and parse an ONIX 3.0 XML file.

  Request:

  `file_name`: The ONIX 3.0 XML file to be parsed.

  Example using curl:

  ```bash
  curl -X POST "http://localhost:8000/parse/" -H "Authorization: Bearer mysecrettoken" -F "file_name=1"
  ```

  This will parse the file named `1.xml` in the sample_data folder and upload the parsed data to AWS MySQL database

  Response:

  - `200 OK` on successful parsing.
  - `400 Bad Request` if the file name is missing or invalid.
  - `404 Bad Request` if the file name is not found.
  - `401 Unauthorized` if the token is invalid.

- GET /countries/{file_name}

  Retrieve the countries for a given parsed ONIX file.

  Request:

  `file_name`: The name of the parsed ONIX file.

  Example using curl:

  ```bash
  curl -X GET "http://localhost:8000/getcountries/1" -H "Authorization: Bearer mysecrettoken"
  ```

  Response:

  - `200 OK` with a JSON object containing the countries.
  - `400 Bad Request` if the file name is missing or invalid.
  - `404 Bad Request` if the file name is not found.
  - `401 Unauthorized` if the token is invalid.

4. Run the tests:

```bash
pytest
```

## Future Improvements

1. **Security**: Using a hard-coded secret-key for now. This can be saved securely as an environment variable. Also this can be enhanced using the Fast API options like OAuth2 with Password (and hashing)
2. **Database connection**: For now database connection string can be accessed in the env file. For security purpose, this can be stored in the secrets.
3. **Typing**: Typing can be used more extensively in the code
4. **Testing**: Add more unit tests and API tests for all the API route handlers.
5. **Folder structure**: For now some files are placed together in the folders that can be placed into a separate folder as we scale the app.
6. **Utils and services**: For now these are placed in the file _parser.py_ but can be placed in a separate file for the sake of reusibility.
