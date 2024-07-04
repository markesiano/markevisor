from abc import ABC
from abc import abstractmethod
class IScreenshot(ABC):
    @abstractmethod
    def take(self, dst, nameImage):
        '''Tomar captura de pantalla y guardarla en dst con el nombre nameImage'''