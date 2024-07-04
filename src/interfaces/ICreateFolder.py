from abc import ABC
from abc import abstractmethod
class ICreateFolder(ABC):
    @abstractmethod
    def create(self, folder):
        '''Crear carpeta'''