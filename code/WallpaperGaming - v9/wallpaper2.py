# Created by A_Aphid

import os, ctypes

WALLPAPEREXE_PATH = fr"C:\Users\{os.getlogin()}\Desktop\WallpaperGaming\wallpaper-x86_64-pc-windows\wallpaper.exe"

def set_wallpaper(path):
    path = os.path.abspath(path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path , 0)

def get_wallpaper():
    result_str = os.popen(f'{WALLPAPEREXE_PATH} get').read().strip()
    return result_str