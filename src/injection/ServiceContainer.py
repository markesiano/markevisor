from interfaces.ICopyFiles import ICopyFiles
from interfaces.ICreateFolder import ICreateFolder
from interfaces.ILogs import ILogs
from interfaces.IScreenshot import IScreenshot
from interfaces.ITakePicture import ITakePicture

# Contenedor de servicios con inversión de dependencias
class ServiceContainer:
    def __init__(self, copy_files_service: ICopyFiles, create_folder_service: ICreateFolder, logs_service: ILogs, screenshot_service: IScreenshot, picture_service: ITakePicture):
        self.copy_files_service = copy_files_service
        self.create_folder_service = create_folder_service
        self.logs_service = logs_service
        self.screenshot_service = screenshot_service
        self.picture_service = picture_service