from fastapi import APIRouter, Request, HTTPException
from .schemas import House, Prediction, CityHouse
from .services import make_prediction

router = APIRouter()


@router.post("/predict/lille", response_model=Prediction, summary="Prédiction pour Lille")
async def get_prediction_lille(house: House, request: Request) -> Prediction:
    """
    Prédit le prix au m² pour un bien immobilier situé à Lille.

    Args:
        house (House): Les caractéristiques du bien (surface, nombre de pièces, etc.).
        request (Request): Requête FastAPI pour accéder aux modèles stockés dans `app.state`.

    Returns:
        Prediction: Le prix estimé au m², le nom du modèle et la ville.
    """
    return await make_prediction(house, "lille", request)


@router.post("/predict/bordeaux", response_model=Prediction, summary="Prédiction pour Bordeaux")
async def get_prediction_bordeaux(house: House, request: Request) -> Prediction:
    """
    Prédit le prix au m² pour un bien immobilier situé à Bordeaux.

    Args:
        house (House): Les caractéristiques du bien.
        request (Request): Objet de requête FastAPI.

    Returns:
        Prediction: Résultat de la prédiction pour Bordeaux.
    """
    return await make_prediction(house, "bordeaux", request)


@router.post("/predict", response_model=Prediction, summary="Prédiction générique par ville")
async def get_prediction(cityhouse: CityHouse, request: Request) -> Prediction:
    """
    Prédit le prix au m² pour un bien immobilier, en fonction de la ville spécifiée.

    Args:
        cityhouse (CityHouse): Objet combinant les caractéristiques du bien et la ville cible.
        request (Request): Objet de requête FastAPI.

    Returns:
        Prediction: Résultat de la prédiction.
    """
    return await make_prediction(cityhouse.features, cityhouse.ville, request)
