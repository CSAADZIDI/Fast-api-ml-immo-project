from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_main():
    response = client.get("/")
    
    
#curl -X POST http://127.0.0.1:8000/predict/lille -H "Content-Type: application/json" -d '{"surface_bati": 100,"nombre_pieces": 4,"surface_terrain": 200,"nombre_lots": 1,"type_local": "Maison"}