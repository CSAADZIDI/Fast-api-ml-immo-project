import joblib
import tempfile
import os
from pathlib import Path

from api import models  # Ton module avec les fonctions

def test_load_model_functions_with_real_file(monkeypatch):
    # Créer un fichier temporaire contenant un faux modèle/scalers
    fake_data = {
        'model_a': "real_model_a",
        'model_m': "real_model_m",
        'scaler_Xa': "real_scaler_Xa",
        'scaler_Xm': "real_scaler_Xm",
        'scaler_ya': "real_scaler_ya",
        'scaler_ym': "real_scaler_ym",
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        pkl_path = Path(tmpdir) / "best_model_lille.pkl"
        joblib.dump(fake_data, pkl_path)

        # Forcer le chemin dans le module à pointer vers ce fichier
        monkeypatch.setattr(models, "models_file", str(pkl_path))

        # Assertions sur les fonctions
        assert models.load_model_a_lille() == "real_model_a"
        assert models.load_model_m_lille() == "real_model_m"
        assert models.load_scaler_Xa_lille() == "real_scaler_Xa"
        assert models.load_scaler_Xm_lille() == "real_scaler_Xm"
        assert models.load_scaler_ya_lille() == "real_scaler_ya"
        assert models.load_scaler_ym_lille() == "real_scaler_ym"
