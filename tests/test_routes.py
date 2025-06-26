import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Request
from unittest.mock import MagicMock

from api.routes import router  # remplace par le chemin correct
from api.schemas import House, CityHouse  # idem

app = FastAPI()
app.include_router(router)

client = TestClient(app)

# Fixture pour mocker request.app.state avec modèles/scalers factices
@pytest.fixture
def mock_models(monkeypatch):
    class DummyScaler:
        def transform(self, X):
            return X * 2  # Ex: double les valeurs pour tester
        def inverse_transform(self, y):
            return y / 2  # Revert le scale (exemple)

    class DummyModel:
        def predict(self, X):
            import numpy as np
            # Retourne la somme des features * 10, par ex.
            return np.array([X.sum(axis=1) * 10])

    # Mock des objets dans app.state
    dummy_scaler = DummyScaler()
    dummy_model = DummyModel()

    class DummyAppState:
        model_a = dummy_model
        scaler_Xa = dummy_scaler
        scaler_ya = dummy_scaler
        model_m = dummy_model
        scaler_Xm = dummy_scaler
        scaler_ym = dummy_scaler

    monkeypatch.setattr(app, "state", DummyAppState())

# Test endpoint /predict/lille avec type_local = "Maison"
def test_predict_lille_maison(mock_models):
    data = {
        "surface_bati": 100,
        "nombre_pieces": 5,
        "type_local": "Maison",
        "surface_terrain": 200,
        "nombre_lots": 1
    }
    response = client.post("/predict/lille", json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["ville_modele"] == "Lille"
    assert "prix_m2_estime" in json_data
    assert json_data["model"] == "DummyModel"

# Test endpoint /predict/lille avec type_local = "Appartement"
def test_predict_lille_appartement(mock_models):
    data = {
        "surface_bati": 80,
        "nombre_pieces": 3,
        "type_local": "Appartement",
        "surface_terrain": 0,
        "nombre_lots": 1
    }
    response = client.post("/predict/lille", json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["ville_modele"] == "Lille"
    assert "prix_m2_estime" in json_data

# Test endpoint /predict/bordeaux avec type_local = "Maison"
def test_predict_bordeaux_maison(mock_models):
    data = {
        "ville": "bordeaux",
        "features": {
            "surface_bati": 120,
            "nombre_pieces": 4,
            "type_local": "Maison",
            "surface_terrain": 250,
            "nombre_lots": 2
        }
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["ville_modele"] == "Bordeaux"
    assert "prix_m2_estime" in json_data

# Test erreur ville non prise en charge
def test_make_prediction_bad_city(mock_models):
    data = {
        "ville": "paris",
        "features": {
            "surface_bati": 100,
            "nombre_pieces": 3,
            "type_local": "Maison",
            "surface_terrain": 100,
            "nombre_lots": 1
        }
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Ville non prise en charge"

# Test erreur type_local non supporté
def test_make_prediction_bad_type_local(mock_models):
    data = {
        "surface_bati": 100,
        "nombre_pieces": 3,
        "type_local": "Chateau",  # type non supporté
        "surface_terrain": 100,
        "nombre_lots": 1
    }
    response = client.post("/predict/lille", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Type de logement non supporté"
