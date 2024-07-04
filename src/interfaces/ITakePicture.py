from abc import ABC
from abc import abstractmethod
class ITakePicture(ABC):
    @abstractmethod
    def take(self, dst, nameImage):
        '''Tomar una foto y guardarla en dst con el nombre nameImage'''