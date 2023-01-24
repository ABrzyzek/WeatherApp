from fastapi.testclient import TestClient
from api.routes import app

client = TestClient(app)

def test_stations_list():
    response = client.get("/stations")
    assert response.status_code == 200
    assert response.json()[0] == {"name": "Warsaw", "code": "EPWA"}
    assert response.json()[1] == {"name": "Gdansk", "code": "EPGD"}

def test_weather():
    response = client.get("/weather")
    assert response.status_code == 200

def test_csv_names():
    response = client.get("/csvs")
    test_file = "test.csv"
    assert response.status_code == 200
    assert test_file in response.json()

def test_dashboard_names():
    response = client.get("/dashboards")
    test_chart = "test_temperature_prediction_chart.png"
    assert response.status_code == 200
    assert test_chart in response.json()