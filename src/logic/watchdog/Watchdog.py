from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time
import os
class WatchdogEventHandler(FileSystemEventHandler):
    def __init__(self, services,backup_folder, screenshot_folder, picture_folder, n_pictures):
        self.services = services
        self.backup_folder = backup_folder
        self.screenshot_folder = screenshot_folder
        self.picture_folder = picture_folder
        self.n_pictures = n_pictures

    def on_modified(self, event):
        if event.is_directory:
            return
        if not self.is_valid_file(event.dest_path):
            return

        self.services.logs_service.savetolog(f'Archivo modificado: {event.src_path}')

        self.services.create_folder_service.create(self.backup_folder)


        self.services.copy_files_service.copy(event.src_path, self.backup_folder)
        self.services.logs_service.savetolog(f'Archivo copiado a {self.backup_folder}')

        self.services.create_folder_service.create(self.screenshot_folder)
        num_files_screenshot_folder = self.get_number_of_files(self.screenshot_folder)
        self.services.screenshot_service.take(self.screenshot_folder, f'screenshot{num_files_screenshot_folder+1}')

        self.services.create_folder_service.create(self.picture_folder)

        num_files_pictures_folder = self.get_number_of_files(self.picture_folder)

        self.take_n_pictures(self.picture_folder, self.n_pictures, num_files_pictures_folder)

            
    def on_created(self, event):
        if event.is_directory:
            return
        if not self.is_valid_file(event.src_path):
            return
        self.services.logs_service.savetolog(f'Archivo creado: {event.src_path}')

        self.services.create_folder_service.create(self.backup_folder)

        self.services.copy_files_service.copy(event.src_path, self.backup_folder)
        self.services.logs_service.savetolog(f'Archivo copiado a {self.backup_folder}')

        self.services.create_folder_service.create(self.screenshot_folder)
        num_files_screenshot_folder = self.get_number_of_files(self.screenshot_folder)
        self.services.screenshot_service.take(self.screenshot_folder, f'screenshot{num_files_screenshot_folder+1}')

        self.services.create_folder_service.create(self.picture_folder)

        num_files_pictures_folder = self.get_number_of_files(self.picture_folder)

        self.take_n_pictures(self.picture_folder, self.n_pictures, num_files_pictures_folder)


    def on_deleted(self, event):
        if event.is_directory:
            return
        if not self.is_valid_file(event.src_path):
            return
        self.services.logs_service.savetolog(f'Archivo eliminado: {event.src_path}')

        self.services.create_folder_service.create(self.screenshot_folder)
        num_files_screenshot_folder = self.get_number_of_files(self.screenshot_folder)
        self.services.screenshot_service.take(self.screenshot_folder, f'screenshot{num_files_screenshot_folder+1}')

        self.services.create_folder_service.create(self.picture_folder)
        num_files_pictures_folder = self.get_number_of_files(self.picture_folder)

        self.take_n_pictures(self.picture_folder, self.n_pictures, num_files_pictures_folder)


    def on_moved(self, event):
        if event.is_directory:
            return
        if not self.is_valid_file(event.src_path):
            return
        self.services.logs_service.savetolog(f'Archivo movido: {event.src_path} a {event.dest_path}')

        self.services.create_folder_service.create(self.backup_folder)

        self.services.copy_files_service.copy(event.src_path, self.backup_folder)
        self.services.logs_service.savetolog(f'Archivo copiado a {self.backup_folder}')

        self.services.create_folder_service.create(self.screenshot_folder)
        num_files_screenshot_folder = self.get_number_of_files(self.screenshot_folder)
        self.services.screenshot_service.take(self.screenshot_folder, f'screenshot{num_files_screenshot_folder+1}')

        self.services.create_folder_service.create(self.picture_folder)
        num_files_pictures_folder = self.get_number_of_files(self.picture_folder)

        self.take_n_pictures(self.picture_folder, self.n_pictures, num_files_pictures_folder)

    def get_number_of_files(self, folder):
        return len([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])

    def take_n_pictures(self, folder, nIterations, nPictures, iteration=0):
        if iteration == nIterations:
            return
        self.services.picture_service.take(folder, f'picture{nPictures}')
        self.take_n_pictures(folder, nIterations, nPictures+1, iteration+1)

    # Funcion que revisa que el archivo tenga formato de imagen, pdf, word, excel, powerpoint, txt, csv, json, xml, mp3, mp4, wav, avi, mov, mkv, zip, rar, 7z, tar, gz, bz2, xz, iso, img, vdi, vmdk
    def is_valid_file(self, file):
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'csv', 'json', 'xml', 'mp3', 'mp4', 'wav', 'avi', 'mov', 'mkv', 'zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz', 'iso', 'img', 'vdi', 'vmdk']
        extension = file.split('.')[-1]
        return extension in valid_extensions
    

class Watchdog:
    def __init__(self, services, watch_folder, backup_folder, screenshot_folder, picture_folder, n_pictures):
        self.services = services
        self.watch_folder = watch_folder
        self.backup_folder = backup_folder
        self.screenshot_folder = screenshot_folder
        self.picture_folder = picture_folder
        self.n_pictures = n_pictures

    def start(self):
        observer = Observer()
        handler = WatchdogEventHandler(self.services, self.backup_folder, self.screenshot_folder, self.picture_folder, self.n_pictures)
        observer.schedule(handler, self.watch_folder, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        