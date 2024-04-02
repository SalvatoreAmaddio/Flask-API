"""
Abstract class for Models
"""
from abc import abstractmethod

class AbstractModel:
    pass

    @abstractmethod
    def readDictionary(self, data:dict):
        """
        This method is used to tell the object how it should read the dictionary.
        It is used to check if all fields have been provided in POST and PUT requests
        """
        pass