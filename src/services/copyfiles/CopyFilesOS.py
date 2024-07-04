import os
from interfaces.ICopyFiles import ICopyFiles
class CopyFilesOS(ICopyFiles):
    def copy(self, src, dst):
        destiny = os.path.join(dst, os.path.basename(src))
        os.system(f'cp {src} {destiny}')
