import Xlib
import Xlib.display
import PIL
from Xlib import X
from PIL import Image


class LinuxCaptureUI(object):
    def __init__(self):
        self.lastRectangle = None
        self.lastHwnd = None

    def ImageCapture(self, rectangle, hwnd):
        x, y, w, h = rectangle
        if w <= 0 or h <= 0 or hwnd == 0:
            raise
        root = Xlib.display.Display().screen().root
        win = Xlib.display.Display().create_resource_object('window', hwnd)
        try:
            geom = win.get_geometry()
        except Exception: #Xlib.error.BadDrawable 
            raise
        if w > geom.width: w = geom.width
        if h > geom.height: h = geom.height
        
        try:
            raw = win.get_image(x,y,w,h,X.ZPixmap, 0xffffffff)
        except Xlib.error.BadMatch:
            raise
        im = Image.frombytes("RGB", (w,h), raw.data, "raw", "BGRX")
        if self.lastRectangle != rectangle:
            self.lastRectangle = rectangle
        if self.lastHwnd != hwnd:
            self.lastHwnd = hwnd
        return im


imgCap = LinuxCaptureUI()


def ImageCapture(rectangle, hwnd):
    global imgCap
    return imgCap.ImageCapture(rectangle, hwnd)


def NextFrame():
    global imgCap
    try:
        im = imgCap.ImageCapture(imgCap.lastRectangle, imgCap.lastHwnd)
    except (Xlib.error.BadMatch, Xlib.error.BadWindow) as ex:
        return False
    return True
