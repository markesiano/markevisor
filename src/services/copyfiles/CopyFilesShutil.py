import shutil
import os
from interfaces.ICopyFiles import ICopyFiles
class CopyFilesShutil(ICopyFiles):
    def copy(self, src, dst):
        try:
            filename = os.path.basename(src)
            destiny = os.path.join(dst, filename)
            shutil.copy(src, destiny)
        except PermissionError:
            pass
