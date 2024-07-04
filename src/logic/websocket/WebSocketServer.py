import asyncio
import websockets
import json
import os
class WebSocketServer:
    def __init__(self, services, backup_folder, screenshot_folder, picture_folder, n_pictures):
        self.services = services
        self.backup_folder = backup_folder
        self.screenshot_folder = screenshot_folder
        self.picture_folder = picture_folder
        self.n_pictures = n_pictures
        
    async def handle_message(self,websocket):
        async for message in websocket:
            # obtenemos los datos filename, finalUrl, url, referrer
            jsonMessage = json.loads(message)
            filename = jsonMessage['filename']
            finalUrl = jsonMessage['finalUrl']
            url = jsonMessage['url']
            referrer = jsonMessage['referrer']
            
            self.services.create_folder_service.create(self.backup_folder)
            
            self.services.logs_service.savetolog(f'filename: {filename}, finalUrl: {finalUrl}, url: {url}, referrer: {referrer}')
            
            self.services.create_folder_service.create(self.screenshot_folder)
            num_files_screenshot_folder = self.get_number_of_files(self.screenshot_folder)
            self.services.screenshot_service.take(self.screenshot_folder, f'screenshot{num_files_screenshot_folder+1}')

            self.services.create_folder_service.create(self.picture_folder)
            num_files_pictures_folder = self.get_number_of_files(self.picture_folder)

            self.take_n_pictures(self.picture_folder, self.n_pictures, num_files_pictures_folder)
        


    async def start_server(self):
        async with websockets.serve(self.handle_message, "localhost", 8000):
            await asyncio.Future()  

    def start(self):
        asyncio.run(self.start_server())      
    
    def get_number_of_files(self, folder):
        return len([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])

    def take_n_pictures(self, folder, nIterations, nPictures, iteration=0):
        if iteration == nIterations:
            return
        self.services.picture_service.take(folder, f'picture{nPictures}')
        self.take_n_pictures(folder, nIterations, nPictures+1, iteration+1)