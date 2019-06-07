modelsFolder = 'KerasModels'

import enum

#TODO: Ajouter les types
#TODO: Faire un enum de tous les models à ajouter, et les fichiers dans lesquels ils sont stockés
#TODO: Pour chaque model, faire une variable "allow_training"
#TODO: Pour chaque model ayant un "allow_training" ajouter:
# - Un tableau contenant les X_train
# - Un tableau contenant les Y_train
# - Une variable disant si le résultat est satisfaisant ou pas

#TODO: Réfléchir à comment rendre cette API simple d'utilisation


class Brain():
    # Loads every keras models
    def __init__(self):
        from .models import model_mucus
        self._auto_training = False


    async def allow_auto_training(self, model):
        self._auto_training = True
    
    async def auto_training(self, model):
        return self._auto_training

    async def on_end(self):
        if not self._auto_training:
            pass
        pass
    
    async def choose(self, model, input):
        """ Launches the wanted model and returns the choice made.
        INPUT: 
            - model: enum defined on this file.
            - input: the input corresponding to the model.
        OUTPUT: depends on which model you choose. """
        pass
    
    async def train(self, model, X_train, Y_train, X_test=None, Y_test=None, *kwargs):
        """ Trains the model according to training input and output datas.
        INPUT: an enum defined on this file.
        OUTPUT: depends on which model you choose. """
        pass

    async def add_training_data(self, model, input, output):
        pass