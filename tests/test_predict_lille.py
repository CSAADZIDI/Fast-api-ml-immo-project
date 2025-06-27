import requests

def test_prediction_lille():
    url = "http://localhost:8000/predict/lille"  
    payload = {
        "surface_bati": 100.0,
        "nombre_pieces": 4,
        "type_local": "appartement",
        "surface_terrain": 0.0,
        "nombre_lots": 1
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "prix_m2_estime" in data
    assert data["ville_modele"].lower() == "lille"
    assert "model" in data

# Pour lancer ce test :cd tests/ puis  python -m pytest test_predict_bordeaux.py
