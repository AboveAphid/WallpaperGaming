# Modified version of: https://forums.pcsx2.net/Thread-Send-key-press-to-inactive-game-window-python-win32api
# Modified by: A_Aphid

from time import sleep
import keyCodes
import win32con
import win32api
import win32gui

class InactiveWindowPresser():
    def __init__(self, windowtitle) -> None:
        
        self.vk_codes = keyCodes.vk_codes

        self.hwnd = win32gui.FindWindow(None, windowtitle)
        if self.hwnd > 0:
            print(f"Main window found! \nHwnd: {self.hwnd}, Window_Text: {win32gui.GetWindowText(self.hwnd)}")
        else:
            print('Main window not found.')
            raise AttributeError

    def getHwnd(self):
        return self.hwnd

    def pressUseWithWrite(self, hwnd, info):
        vk_key, delay = info
        if vk_key == str(vk_key).upper():
            win32api.PostMessage(hwnd, win32con.WM_CHAR, self.vk_codes[str(vk_key).lower()], 0) # Sends capital letter Q
        elif 1 == 1:
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, self.vk_codes[vk_key], 0) # Presses the letter Q (not capitalised)
        else:
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, self.vk_codes[vk_key], 0) # Presses the letter Q (not capitalised)
        
        sleep(delay) # Allow time for press to register

    def press(self, key, delay=0.1):
        print('Pressing:', key, self.vk_codes[key])
        if key == str(key).upper():
            win32api.PostMessage(self.hwnd, win32con.WM_CHAR, self.vk_codes[str(key).lower()], 0) # Sends capital letter Q
        else:
            # Use instead of PostMessage (PostMessage does work but can be buggy and only work the first couple of times)
            win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, self.vk_codes[key], 0) # Presses the letter Q (not capitalised) 
            sleep(0.1)
            win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, self.vk_codes[key], 0) # Presses the letter Q (not capitalised)

    def hold(self, key, holdlength=3, delay=0.1):
        print('Holding:', key, self.vk_codes[key])
        if key == str(key).upper():
            win32api.PostMessage(self.hwnd, win32con.WM_CHAR, self.vk_codes[str(key).lower()], 0) # Sends capital letter Q
        else:
            # Use instead of PostMessage (PostMessage does work but can be buggy and only work the first couple of times)
            win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, self.vk_codes[key], 0) # Presses the letter Q (not capitalised) 
            sleep(holdlength)
            win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, self.vk_codes[key], 0) # Presses the letter Q (not capitalised)

        
        sleep(delay) # Allow time for press to register

    def write(self, keys:list, delay=0.1):
        for vk_key in keys:
            print(vk_key)
            win32gui.EnumChildWindows(self.hwnd, self.pressUseWithWrite, (vk_key, delay))
        

################################
            
if __name__ == '__main__':
    win_title = "Untitled - Notepad"



    inactiveAccessor = InactiveWindowPresser(win_title)

    inactiveAccessor.write(['H', 'e', 'l', 'l', 'o', ',', 'spacebar', 'h', 'o', 'w', 'spacebar', 'a', 'r', 'e', 'spacebar', 'y', 'o', 'u', '?'],
                        delay=0.02)