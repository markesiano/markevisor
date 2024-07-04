import os
from interfaces.ICreateFolder import ICreateFolder
class CreateFolderOs(ICreateFolder):
    def create(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)