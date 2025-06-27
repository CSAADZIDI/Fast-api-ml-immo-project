from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routes import router
from .models import (
    load_model_a_lille,
    load_model_m_lille,
    load_scaler_Xa_lille,
    load_scaler_Xm_lille,
    load_scaler_ya_lille,
    load_scaler_ym_lille,
    load_model_a_bordeaux,
    load_model_m_bordeaux,
)

app = FastAPI(
    title="Welcome to the Price Prediction Application",
    description="Cette API permet d'estimer le prix au mètre carré d'un bien immobilier "
                "(appartement ou maison) en fonction de ses caractéristiques.",
    version="1.0.0",
)

# Chargement des modèles et scalers en mémoire au démarrage de l'application.
# Ces objets sont stockés dans l'état de l'application (app.state)
# pour être accessibles dans toutes les requêtes sans les recharger à chaque appel.
app.state.model_a = load_model_a_lille()
app.state.model_m = load_model_m_lille()
app.state.scaler_Xa = load_scaler_Xa_lille()
app.state.scaler_Xm = load_scaler_Xm_lille()
app.state.scaler_ya = load_scaler_ya_lille()
app.state.scaler_ym = load_scaler_ym_lille()
app.state.model_a_b = load_model_a_bordeaux()
app.state.model_m_b = load_model_m_bordeaux()

# Inclusion des routes définies dans le module `routes`
app.include_router(router)

@app.get("/", include_in_schema=False)
async def root():
    """
    Redirige automatiquement la racine de l'application vers la documentation interactive (/docs).
    """
    return RedirectResponse(url="/docs")
