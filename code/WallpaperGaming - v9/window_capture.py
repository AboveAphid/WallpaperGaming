# Modified version of: https://www.youtube.com/watch?v=7k4j-uL8WSQ
# Modified by: A_Aphid

import win32gui, win32ui, win32con, numpy as np, ctypes
from ctypes import windll
from PIL import Image

class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name=None):
        # find the handle for the window we want to capture.
        # if no window name is given, capture the entire screen
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        # Uncomment the following line if you use a high DPI display or >100% scaling size
        # windll.user32.SetProcessDPIAware()

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y



    def convertPILToCv2(self, pil_img:Image):
        open_cv_image = np.array(pil_img)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        return open_cv_image

    @staticmethod
    def checkVisibility(hwnd):
        window = hwnd
        if window:
            tup = win32gui.GetWindowPlacement(window)
        if tup[1] == win32con.SW_SHOWMAXIMIZED:
            normal = False
            minimized = False
            maximized = True
        elif tup[1] == win32con.SW_SHOWMINIMIZED:
            normal = False
            minimized = True
            maximized = False
        elif tup[1] == win32con.SW_SHOWNORMAL:
            normal = True
            minimized = False
            maximized = False
        return (minimized, maximized, normal)

    def forceMinimised(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, win32con.SW_SHOWMINIMIZED)

    def forceMaximised(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, win32con.SW_SHOWMAXIMIZED)
    
    def forceNotActive(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, win32con.SW_SHOWNOACTIVATE)

    def get_screenshot(self, addedX=0, addedY=0):
        # Get the window dimensions
        if self.checkVisibility(self.hwnd)[0] == True:
            print("Please don't minimize window.")
            self.forceNotActive()
            # ctypes.windll.user32.ShowWindow(self.hwnd, 6)

        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        width = right - left + addedX
        height = bot - top + addedY

        # Create a device context for the window
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        # Create a bitmap to store the window contents
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)


        # Use PrintWindow to capture the window contents
        #result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 0) # Sometimes returns a black screen for windows
        result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 3) # USE 3 NOT 0 - Otherwise some windows may retrieve a black screen. E.g. OBS


        if result == 0:
            # PrintWindow failed, possibly due to the window being on another display
            print("PrintWindow failed")
            return None

        # Convert the bitmap to a PIL image
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # Clean up
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)

        # img.save('screenshot.png')

        return self.convertPILToCv2(img)


    def get_screenshotOLD(self):
        # Get the window dimensions
        if self.checkVisibility(self.hwnd)[0] == True:
            print("Please don't minimize window.")
            # ctypes.windll.user32.ShowWindow(self.hwnd, 6)
            self.forceNotActive()

        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        width = right - left
        height = bot - top

        # Create a device context
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        # Create a bitmap and select it into the device context
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)

        # Copy the window image to the bitmap
        result = win32gui.BitBlt(saveDC.GetSafeHdc(), 0, 0, width, height, hwndDC, 0, 0, win32con.SRCCOPY)

        # Save the bitmap to a file
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # Clean up
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)

        return self.convertPILToCv2(img)

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
    



if __name__ == '__main__':
    import cv2
    
    WindowCapture.list_window_names()

    print('\n---------------------------------------\n')
        
    appCap = WindowCapture('SpaceIdle')
    
    while 1:

        img = appCap.get_screenshot()

        cv2.imshow('Screenshot', img)

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break