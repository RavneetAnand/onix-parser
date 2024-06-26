# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

# Set environment variables
ENV DATABASE_URL=mysql+pymysql://admin:PVgYGe7Jk90Wwk7CRO21@mybooksdb.cfwg6i8sestu.eu-west-2.rds.amazonaws.com:3306/DBDBOOKS

EXPOSE 3000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden.
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
