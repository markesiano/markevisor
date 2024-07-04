from abc import ABC
from abc import abstractmethod
class ICopyFiles(ABC):
    @abstractmethod
    def copy(self, src, dst):
        '''Copiar archivos de src a dst'''