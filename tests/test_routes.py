from fastapi.testclient import TestClient
from api.routes import app
from datetime import datetime

client = TestClient(app)

def test_stations_list():
    response = client.get("/stations")
    assert response.status_code == 200
    assert response.json()[0] == {"name": "Warsaw", "code": "EPWA"}
    assert response.json()[1] == {"name": "Gdansk", "code": "EPGD"}

def test_station():
    response = client.get("/weather/test")
    date = datetime(2023,1,1)
    date = date.isoformat()
    assert response.status_code == 200
    assert response.json()[0] == {"date":date, "city":"Warsaw", "temperature":57, "dev_point":48, "humidity":72, "wind":"SW", "wind_speed":10, "wind_gust":None, "pressure":29.57, "precipitation":None, "visibility":6, "heat_index":57, "weather_status":"Fair", "user_notes":None}

def test_chart():
    response = client.get("/chart/test")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_chart_invalid_variable():
    response = client.get("/chart/invalid")
    assert response.json() == {"error":"file_not_found"}
    