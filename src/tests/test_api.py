from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

# Create a TestClient instance
client = TestClient(app)

# Test API getcountries with a valid file
def test_getcountries_valid_file():
    response = client.get("/getcountries/2")
    assert response.status_code == 200
    assert response.json() == {
        "countries": [
            "Canada",
            "Denmark",
            "France",
            "Germany",
            "Ireland",
            "United Kingdom",
            "United States"
        ]
    }

# Test API getcountries with an empty file name
def test_getcountries_empty_file():
    response = client.get("/getcountries/ ")
    assert response.status_code == 400
    assert response.json() == {"detail": "File name is required"}

# Test API getcountries with an invalid file name
def test_getcountries_invalid_file():
    response = client.get("/getcountries/5")
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}

# Test API parse with a valid file
def test_parse_file_valid():
    with patch('main.parse_onix') as mock_parse_onix:
        response = client.post("/parse/", params={"file_name": "2"})
        assert response.status_code == 200
        assert response.json() == {"status": "file parsed successfully"}
        mock_parse_onix.assert_called_once_with("sample_data/2.xml")

# Test API parse with an empty file name
def test_parse_file_invalid():
    response = client.post("/parse/", params={"file_name": " "})
    assert response.status_code == 400
    assert response.json() == {"detail": "File name is required"}

# Test API parse with an invalid file name
def test_parse_file_exception():
    with patch('main.parse_onix', side_effect=Exception("Parse error")):
        response = client.post("/parse/", params={"file_name": "1"})
        assert response.status_code == 500
        assert "Parse error" in response.text