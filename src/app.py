import tkinter as tk
from tkinter import filedialog
import threading
import os

from injection.ServiceContainer import ServiceContainer
from services.copyfiles.CopyFilesShutil import CopyFilesShutil
from services.createfolder.CreateFolderOs import CreateFolderOs
from services.logs.LogsLogging import LogsLogging
from services.screenshots.ScreenshotPyautogui import ScreenshotPyautogui
from services.pictures.TakePictureOpencv import TakePictureOpencv

from logic.websocket.WebSocketServer import WebSocketServer
from logic.watchdog.Watchdog import Watchdog

watchdog_thread = None
websocket_thread = None

if __name__ == "__main__":

    def select_folder(label):
        global folder_to_watch, backup_folder
        folder_selected = filedialog.askdirectory()
        label.config(text=folder_selected)
        if label == backup_label:
            backup_folder = folder_selected
        else:
            folder_to_watch = folder_selected
        check_button_state()

    def start():
        global folder_to_watch, backup_folder, watchdog_thread, websocket_thread
        SCREENSHOT = "screenshots"
        PICTURE = "pictures"
        BACKUP = "backup"

        backup_folder = os.path.join(backup_folder, BACKUP)
        screenshot_folder = os.path.join(backup_folder, SCREENSHOT)
        picture_folder = os.path.join(backup_folder, PICTURE)
        n_pictures = 5
        services = ServiceContainer(CopyFilesShutil(), CreateFolderOs(), LogsLogging(backup_folder), ScreenshotPyautogui(), TakePictureOpencv())

        def start_websocket_server():
            websocketserver = WebSocketServer(services, backup_folder, screenshot_folder, picture_folder, n_pictures)
            websocketserver.start()

        def start_watchdog():
            watchdog = Watchdog(services, folder_to_watch, backup_folder, screenshot_folder, picture_folder, n_pictures)
            watchdog.start()

        try:
            watchdog_thread = threading.Thread(target=start_watchdog)
            websocket_thread = threading.Thread(target=start_websocket_server)
            watchdog_thread.start()
            websocket_thread.start()
        except Exception as e:
            print("Error al iniciar hilos:", e)
            stop_threads()
        else:
            root.destroy()

    def stop_threads():
        global watchdog_thread, websocket_thread
        if watchdog_thread:
            watchdog_thread.join()
        if websocket_thread:
            websocket_thread.join()

    def check_button_state():
        if folder_to_watch and backup_folder and folder_to_watch != backup_folder:
            start_button.config(state=tk.NORMAL)
        else:
            start_button.config(state=tk.DISABLED)

    root = tk.Tk()
    root.title("Seleccionar Carpetas")

    window_width = 300
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    root.resizable(False, False)

    folder_to_watch = ""
    backup_folder = ""

    folder_watch_label = tk.Label(root, text="Seleccionar carpeta para observar")
    folder_watch_label.place(x=10, y=20)

    folder_watch_button = tk.Button(root, text="Seleccionar", command=lambda: select_folder(folder_watch_label))
    folder_watch_button.place(x=220, y=15)

    backup_label = tk.Label(root, text="Seleccionar carpeta para almacenar")
    backup_label.place(x=10, y=60)

    backup_button = tk.Button(root, text="Seleccionar", command=lambda: select_folder(backup_label))
    backup_button.place(x=220, y=55)

    start_button = tk.Button(root, text="Iniciar", command=start, state=tk.DISABLED)
    start_button.place(x=120, y=100)

    root.mainloop()

    stop_threads()
