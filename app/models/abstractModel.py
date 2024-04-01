from abc import abstractmethod

class AbstractModel:
    pass

    @abstractmethod
    def readDictionary(self, data:dict):
        pass