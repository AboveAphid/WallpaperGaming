# Created by A_Aphid

import win32gui, time, keyboard, tkinter as tk, sys
from tkinter import Button, StringVar, Tk, Label, OptionMenu, Checkbutton, messagebox, Scale, Entry
from WallpaperGaming import WallpaperGaming
from win32api import GetSystemMetrics
from threading import Thread

EXITED = False
hwnd = ''

showCV2 = True


# Create object 
root = Tk() 

root.title('Wallpaper Gaming v10')

root.iconbitmap("logo.ico")

# Adjust size 
root.geometry("400x650") 

# datatype of menu text 
clicked = StringVar() 

def get_window_names() -> list:
    """
    Returns a list of available window names
    """
    windows = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
            windows.append(win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)
    return windows

# Change the label text 
def changeWindow(newText) -> None:
    """
    Changes choosen window from window dropdown
    """
    global hwnd, wallpaperGaming
    window_name = newText

    try:
        hwnd = win32gui.FindWindow(None, window_name)
    except:
        hwnd = 'N/A'

    choosenLabel.config(text = f"Choosen: {window_name}") 
    choosenhWndLabel.config(text = f"hWnd: {hwnd}") 

    clicked.set(window_name)

    # if window_name == "UNDERTALE":
    #     wallpaperGaming = WallpaperGaming(window_name, extraX=280, extraY=200, showCV2Window=showCV2)
    # else:
    wallpaperGaming = WallpaperGaming(window_name, showCV2Window=showCV2, extraX=int(extraXScale.get()), extraY=int(extraYScale.get()))
    

def updateWindowOptions() -> None:
    """
    Update window dropdown options
    """
    global windows, drop

    windows = get_window_names()

    drop['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    for choice in windows:
        drop['menu'].add_command(label=choice, command=tk._setit(StringVar(), choice, changeWindow))


wallpaperGamingThread = None
def start() -> None:
    """
    Runs main code
    """
    try:
        global wallpaperGaming, wallpaperGamingThread, showCV2WindowIntVar, showFPSIntVar, extraXScale, extraYScale, showAlertBoxesIntVar
        
        if showCV2WindowIntVar.get() == 1:
            showCV2 = True
        else:
            showCV2 = False
        if showFPSIntVar.get() == 1:
            showFPS = True
        else:
            showFPS = False
        if showAlertBoxesIntVar.get() == 1:
            showAlertBoxes = True
        else:
            showAlertBoxes = False

        wallpaperGamingThread = Thread(target=wallpaperGaming.start, args=(showCV2,showFPS,FPSLabel, extraXScale.get(), extraYScale.get(), showAlertBoxes))

        wallpaperGamingThread.start()

        messagebox.showinfo('WallpaperGaming', 'Now running!')


    except AttributeError as e:
        messagebox.showwarning('WallpaperGaming', f'Make sure to specify game window!')
    except Exception as e:
        messagebox.showerror('WallpaperGaming', f'Failed to launch! Error: {e}')
    

class placeholder():
    """
    Is used as a placeholder class for wallpaperGaming when user hasn't selected a window yet.
    """
    def exit(self, root:Tk) -> None:
        try:
            root.destroy()
        except:
            pass

wallpaperGaming = placeholder()
def stop() -> None:
    """
    Stops program
    """
    root.destroy()

    global wallpaperGaming
    try:
        wallpaperGaming.exit(root)
    except Exception as e:
        print('Stop error:', e)


    # ISSUE WITH BELOW CODE 
    if wallpaperGamingThread:
        print('Joining thread...')
        wallpaperGamingThread.join(timeout=5)
        print('Thread terminated.')

    if showAlertBoxesIntVar.get() == 1:
        messagebox.showinfo('GUI Closed')

    sys.exit(0)


# initial menu text 
clicked.set("N/A")

windows = get_window_names()


# Create Dropdown menu 
drop = OptionMenu(root, clicked, *windows, command=changeWindow) 
drop.grid(row=1, column=0)

# Create Labels
choosenLabel = Label(root, text = "Choosen: N/A") 
choosenLabel.grid(row=2, column=0)
choosenhWndLabel = Label(root, text = "hWnd: N/A") 
choosenhWndLabel.grid(row=3, column=0)

# Create checkboxs
showCV2WindowIntVar = tk.IntVar()
showCV2WindowCheckBox = Checkbutton(root, text = "Show CV2 Window", 
                                       variable = showCV2WindowIntVar,
                                       onvalue = 1, offvalue = 0, height=5, 
                                       width = 20)
showCV2WindowCheckBox.grid(row=4, column=0, padx=100)

showFPSIntVar = tk.IntVar()
showFPSCheckBox = Checkbutton(root, text = "FPS", 
                                       variable = showFPSIntVar,
                                       onvalue = 1, offvalue = 0, height=5, 
                                       width = 20)
showFPSCheckBox.grid(row=5, column=0)

showAlertBoxesIntVar = tk.IntVar()
showAlertBoxesCheckBox = Checkbutton(root, text = "Show alerts", 
                                       variable = showAlertBoxesIntVar,
                                       onvalue = 1, offvalue = 0, height=5, 
                                       width = 20)
showAlertBoxesIntVar.set(1)
showAlertBoxesCheckBox.grid(row=6, column=0)

def extraXChangeScale(val) -> None:
    global extraXScale
    extraXEntry.delete(0, tk.END)
    extraXEntry.insert(0, val)

def extraXChangeEntry(val) -> None:
    global extraXEntry
    try:
        extraXScale.set(extraXEntry.get())
    except:
        # Delete last char since it was probably a letter not int
        extraXEntry.delete(len(extraXEntry.get())-1, tk.END)
        # extraXEntry.insert(len(extraXEntry.get())-1, " ")

def extraYChangeScale(val) -> None:
    global extraYScale
    extraYEntry.delete(0, tk.END)
    extraYEntry.insert(tk.END, val)

def extraYChangeEntry(val) -> None:
    global extraYEntry
    print(len(extraYEntry.get()))
    try:
        extraYScale.set(extraYEntry.get())
    except:
        # Delete last char since it was probably a letter not int
        extraYEntry.delete(len(extraYEntry.get())-1, tk.END)
        # extraYEntry.insert(len(extraYEntry.get())-1, " ")

# Create Scales
Label(root, text="ExtraX").grid(row=7, column=0)
extraXScale = Scale(root, from_=0, to=800, orient=tk.HORIZONTAL, length=200, command=lambda val: extraXChangeScale(val))
extraXScale.set(0)
extraXScale.grid(row=8, column=0)

extraXEntry=Entry(root, width=35)
extraXEntry.bind("<KeyRelease>", extraXChangeEntry)   
extraXEntry.grid(row=9, column=0)

Label(root, text="ExtraY").grid(row=10, column=0)
extraYScale = Scale(root, from_=0, to=800, orient=tk.HORIZONTAL, length=200, command=lambda val: extraYChangeScale(val))
extraYScale.set(0)
extraYScale.grid(row=11, column=0)

extraYEntry=Entry(root, width=35)
extraYEntry.bind("<KeyRelease>", extraYChangeEntry)   
extraYEntry.grid(row=12, column=0)

Label(root, text="Stats").grid(row=13, column=0)
FPSLabel = Label(root, text="FPS: N/A")
FPSLabel.grid(row=14, column=0, pady=10, sticky=tk.N)

# Create btns
updateWindowOptionsBtn = Button(root, text="Update windows options", command=updateWindowOptions)
updateWindowOptionsBtn.grid(row=15, column=0)

startBtn = Button(root, text="Start", command=start)
startBtn.grid(row=16, column=0, padx=160, sticky=tk.W)

stopBtn = Button(root, text="Stop", command=stop)
stopBtn.grid(row=16, column=0, padx=160, sticky=tk.E)

CreditsLabel = Label(root, text="Created by A_Aphid (YT)")
CreditsLabel.grid(row=17, column=0)

Label(root, text="Check out my YT channel for tutorial on how to use!").grid(row=18, column=0)


HiddenCredits = Label(root, text="Hidden Credits: Created by A_Aphid (YT). Just incase you trying to play me.") # Ik this is easy to bypass. I'm just saying its not cool to claim things as your own. Altleast credit the author man. Its not that hard.
HiddenCredits.grid(row=50, column=0, pady=100)

root.mainloop() 

EXITED = True
hwnd = ''

wallpaperGaming.exit(root)

try:
    root.destroy()
except:
    pass

print('Window Exited.')

if showAlertBoxesIntVar.get() == 1:
    messagebox.showinfo('GUI Closed')

sys.exit(0)