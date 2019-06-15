import keras
from keras.models import load_model
import os

from .models_id import *

MOD_DIR = "KerasModels"

async def mod_creep_expension_queen(file="CREEP_EXPENSION_QUEEN"):
    path = os.path.normpath(MOD_DIR+'/'+file)
    if os.path.isfile(path):
        return load_model(file)
    return None #TODO

async def mod_creep_expension_tumor(file="CREEP_EXPENSION_TUMOR"):
    path = os.path.normpath(MOD_DIR+'/'+file)
    if os.path.isfile(path):
        return load_model(file)
    return None

async def mod_creep_expension_overlord(file="CREEP_EXPENSION_OVERLORD"):
    path = os.path.normpath(MOD_DIR+'/'+file)
    if os.path.isfile(path):
        return load_model(file)
    return None

# Main function
def model_select(self, model: ModelTypeId):
    if model == CREEP_EXPENSION_QUEEN:
        return mod_creep_expension_queen()

    elif model == CREEP_EXPENSION_TUMOR:
        return mod_creep_expension_tumor()

    elif model == CREEP_EXPENSION_OVERLORD:
        return mod_creep_expension_overlord()