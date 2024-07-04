import logging
from interfaces.ILogs import ILogs
import getpass
from interfaces.ICreateFolder import ICreateFolder
from services.createfolder.CreateFolderOs import CreateFolderOs

class LogsLogging(ILogs):
    def __init__(self,backup_folder, create_folder_service: ICreateFolder = CreateFolderOs()):
        self.user = getpass.getuser()
        self.backup_folder = backup_folder
        self.create_folder_service = create_folder_service        
        self.initConfig()

        
        
    def initConfig(self):
        folder_name = self.backup_folder+'/log'
        self.create_folder_service.create(folder_name)
        log_name = folder_name + '/log.dev'
        logging.basicConfig(filename=log_name, filemode='a', level=logging.INFO, format='%(asctime)s | %(process)d | %(message)s' + f' | user: {self.user}', datefmt='%Y-%m-%d %H:%M:%S')

    def savetolog(self, message):
        logging.info(message)