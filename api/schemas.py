from pydantic import BaseModel
from typing import Literal



class House(BaseModel):
    surface_bati: float
    nombre_pieces : int # 4
    type_local: str#Literal["appartement", "maison"]
    surface_terrain: float
    nombre_lots: int

class CityHouse(BaseModel):
    ville: str#Literal["lille", "bordeaux"]
    features: House   

class Prediction(BaseModel):
    prix_m2_estime: float
    ville_modele :  str #"Lille", "Bordeaux"
    model: str #"RandomForestRegressor"
