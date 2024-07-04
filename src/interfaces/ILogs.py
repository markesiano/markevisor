from abc import ABC
from abc import abstractmethod
class ILogs(ABC):
    @abstractmethod
    def savetolog(self, message):
        '''Guardar mensaje en un log'''