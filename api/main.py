from fastapi import FastAPI
from .routes import router
from fastapi.responses import RedirectResponse
from .models import load_model_a_lille,load_model_m_lille,load_scaler_Xa_lille,load_scaler_Xm_lille,load_scaler_ya_lille,load_scaler_ym_lille



app = FastAPI(
    title= "Welcome to the Price Prediction Application"
)

# Charger les modèles une seule fois
app.state.model_a = load_model_a_lille()
app.state.model_m = load_model_m_lille()
app.state.scaler_Xa = load_scaler_Xa_lille()
app.state.scaler_Xm = load_scaler_Xm_lille()
app.state.scaler_ya = load_scaler_ya_lille()
app.state.scaler_ym = load_scaler_ym_lille()

# Monter les routes
app.include_router(router)

# Redirection depuis la racine vers /docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")