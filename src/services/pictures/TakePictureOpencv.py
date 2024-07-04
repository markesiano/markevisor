import cv2
from interfaces.ITakePicture import ITakePicture
class TakePictureOpencv(ITakePicture):
    def take(self, dst, nameImage):
        try:
            camera = cv2.VideoCapture(0)
            _, image = camera.read()
            cv2.imwrite(f'{dst}/{nameImage}.png', image)
            del(camera)
            return True
        except Exception as e:
            return False