"""
Este módulo contiene la clase Cache, que permite almacenar y recuperar datos en un archivo JSON.
IMPORTANTE: NO USAR EN PRODUCCION
"""


import json
import os


class Cache:
    def __init__(self, id: str | None = None, directory: str = "./datos/_cache"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self._id = id
        self.directory = directory
        self.path = os.path.join(self.directory, f"{self.id}.json")

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        self.path = os.path.join(self.directory, f"{self.id}.json")

    def save(self, data: dict | list):
        with open(self.path, "w") as f:
            json.dump(data, f)

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def exists(self):
        return os.path.exists(self.path)
