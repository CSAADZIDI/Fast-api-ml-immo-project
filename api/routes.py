from fastapi import APIRouter, Request, HTTPException
from .schemas import House, Prediction, CityHouse
import numpy as np

router = APIRouter()

def make_prediction(data: House, city_name: str, request: Request) -> Prediction:
    if city_name.lower() == "lille":
        return _predict(data, request, "lille")
    elif city_name.lower() == "bordeaux":
        return _predict(data, request, "bordeaux")
    else:
        raise HTTPException(status_code=400, detail="Ville non prise en charge")

def _predict(house: House, request: Request, ville: str) -> Prediction:
    house_array = np.array([[house.surface_bati, house.nombre_pieces, house.surface_terrain, house.nombre_lots]])

    if house.type_local.lower() == "appartement":
        model = request.app.state.model_a #if ville == "lille" else request.app.state.model_a_bx
        scaler_X = request.app.state.scaler_Xa #if ville == "lille" else request.app.state.scaler_Xa_bx
        scaler_y = request.app.state.scaler_ya #if ville == "lille" else request.app.state.scaler_ya_bx

    elif house.type_local.lower() == "maison":
        model = request.app.state.model_m #if ville == "lille" else request.app.state.model_m_bx
        scaler_X = request.app.state.scaler_Xm #if ville == "lille" else request.app.state.scaler_Xm_bx
        scaler_y = request.app.state.scaler_ym #if ville == "lille" else request.app.state.scaler_ym_bx

    else:
        raise HTTPException(status_code=400, detail="Type de logement non supporté")

    input_scaled = scaler_X.transform(house_array)
    output_scaled = model.predict(input_scaled)
    output = scaler_y.inverse_transform(output_scaled.reshape(1, -1))

    return Prediction(
        prix_m2_estime=output[0][0],
        ville_modele=ville.capitalize(),
        model=type(model).__name__
    )

# Endpoints

@router.post("/predict/lille", response_model=Prediction)
def get_prediction_lille(house: House, request: Request):
    return make_prediction(house, "lille", request)

@router.post("/predict/bordeaux", response_model=Prediction)
def get_prediction_bordeaux(house: House, request: Request):
    return make_prediction(house, "bordeaux", request)

@router.post("/predict", response_model=Prediction)
def get_prediction(cityhouse: CityHouse, request: Request):
    return make_prediction(cityhouse.features, cityhouse.ville, request)

        