# SRC: https://www.youtube.com/watch?v=a9F_ZKaYCN4&list=PLqipd5tdUH84Tab9SPFBOWBcW_LTpNoSk&index=5

import win32gui, win32api, win32con, time

def clickWindow(windowName, x, y) -> None:
    """
    Virtually (left) clicks on specific window
    """

    hWnd = win32gui.FindWindow(None, windowName)
    hWnd = win32gui.FindWindowEx(hWnd, None, None, None)

    click = win32api.MAKELONG(x, y)
    print(x, y, click)

    win32gui.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, click)
    win32gui.SendMessage(hWnd, win32con.WM_LBUTTONUP, None, click)
    time.sleep(0.5)
    

if __name__ == "__main__":
    window_name = 'SpaceIdle'
    X, Y = (100,50)

    clickWindow(window_name, X, Y)