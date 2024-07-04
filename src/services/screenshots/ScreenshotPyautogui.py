import pyautogui
from interfaces.IScreenshot import IScreenshot
class ScreenshotPyautogui(IScreenshot):
    def take(self, dst, nameImage):
        image = pyautogui.screenshot()
        image.save(f'{dst}/{nameImage}.png')