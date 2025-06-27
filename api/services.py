from fastapi import Request, HTTPException
from .schemas import House, Prediction, CityHouse
import numpy as np
import asyncio

async def make_prediction(data: House, city_name: str, request: Request) -> Prediction:
    """
    Effectue une prédiction du prix au m² pour un bien immobilier donné dans une ville supportée.

    Cette fonction est asynchrone et délègue la prédiction réelle à la fonction `_predict` 
    en utilisant `asyncio.to_thread` pour ne pas bloquer l'exécution async.

    Args:
        data (House): Les caractéristiques du logement pour lequel on souhaite prédire le prix.
        city_name (str): Le nom de la ville (ex. "lille" ou "bordeaux").
        request (Request): L'objet Request FastAPI, utilisé ici pour accéder aux modèles et scalers chargés.

    Raises:
        HTTPException: Si la ville n'est pas prise en charge.

    Returns:
        Prediction: Le résultat de la prédiction contenant le prix estimé, la ville et le type de modèle utilisé.
    """
    if city_name.lower() not in {"lille", "bordeaux"}:
        raise HTTPException(status_code=400, detail="Ville non prise en charge")
    return await asyncio.to_thread(_predict, data, request, city_name.lower())


def _predict(house: House, request: Request, ville: str) -> Prediction:
    """
    Effectue la prédiction synchrone du prix au m² sur la base des caractéristiques du logement.

    Args:
        house (House): Les caractéristiques du logement.
        request (Request): L'objet Request FastAPI, permettant d'accéder aux modèles et scalers chargés dans l'application.
        ville (str): Le nom de la ville en minuscules ("lille" ou "bordeaux").

    Raises:
        HTTPException: Si le type de logement n'est pas supporté.

    Returns:
        Prediction: Le résultat de la prédiction avec le prix estimé, la ville et le nom du modèle utilisé.
    """
    
    
    house_array = np.array([[house.surface_bati, house.nombre_pieces, house.surface_terrain, house.nombre_lots]])

    if house.type_local.lower() == "appartement":
        model = request.app.state.model_a if ville == "lille" else request.app.state.model_a_b
        scaler_X = request.app.state.scaler_Xa 
        scaler_y = request.app.state.scaler_ya 

    elif house.type_local.lower() == "maison":
        model = request.app.state.model_m if ville == "lille" else request.app.state.model_m_b
        scaler_X = request.app.state.scaler_Xm 
        scaler_y = request.app.state.scaler_ym 

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