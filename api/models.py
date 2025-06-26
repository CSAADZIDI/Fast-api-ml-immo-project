import joblib 
import os

import sys


models_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/','best_model_lille.pkl' ))

def load_model_a_lille():
    loaded_model_a = joblib.load(models_file)['model_a']
    return loaded_model_a

def load_scaler_Xa_lille():   
    loaded_scaler_Xa = joblib.load(models_file)['scaler_Xa']
    return loaded_scaler_Xa

def load_scaler_ya_lille():
    loaded_scaler_ya = joblib.load(models_file)['scaler_ya']
    return loaded_scaler_ya

def load_model_m_lille():
    loaded_model_m = joblib.load(models_file)['model_m']
    return loaded_model_m

def load_scaler_Xm_lille():
    loaded_scaler_Xm = joblib.load(models_file)['scaler_Xm']
    return loaded_scaler_Xm

def load_scaler_ym_lille():
    loaded_scaler_ym = joblib.load(models_file)['scaler_ym']
    return loaded_scaler_ym
   


    
    
    