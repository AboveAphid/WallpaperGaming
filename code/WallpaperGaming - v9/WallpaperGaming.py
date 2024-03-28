# Created by A_Aphid

import window_capture, wallpaper2, time, sendKeyPresses, sendCursorPress, keyboard, convertKeycodes
import cv2, sys, tkinter as tk
from tkinter import messagebox
from threading import Thread

class WallpaperGaming():

    def __init__(self, gameWindowName, extraX=0, extraY=0, showCV2Window=False) -> None:

        self.GAME_WINDOW_NAME = gameWindowName

        self.ADDED_X_TO_SCREEN_CAPTURE = extraX # Default to 0 # Undertale Recommended: 280
        self.ADDED_Y_TO_SCREEN_CAPTURE = extraY # Default to 0 # Undertale Recommended: 200

        self.BEFORE_BG = wallpaper2.get_wallpaper()

        self.EXITED = False

        self.PREV_processTime = 0

        self.SHOWCV2WINDOW = showCV2Window

        print('Default background path:', self.BEFORE_BG)

        self.capture = window_capture.WindowCapture(self.GAME_WINDOW_NAME)
        self.keyPresser = sendKeyPresses.InactiveWindowPresser(self.GAME_WINDOW_NAME)

        self.showProcessTime = False
        self.showFPS = False
        self.ignoreErrors = False
        self.showAlertBoxes = True

        self.pressing = []





    def keyPressed(self, a:keyboard.KeyboardEvent):
        if self.EXITED:
            return

                
        
        def code(self:WallpaperGaming, a:keyboard.KeyboardEvent):
            keyname = a.name
            
            if len(self.pressing) > 2:
                self.pressing.clear()
                self.pressing.append(keyname)

            elif keyname in self.pressing:
                return

            else:
                self.pressing.append(keyname)

            time.sleep(0.5)

            vk_key = convertKeycodes.convertToVk_key(keyname)

            if vk_key == None:
                print('UNKNOWN KEY PRESSED! Keyname:', keyname)
                return

            try:
                self.pressing.remove(keyname)
            except ValueError:
                print('Failed to remove')
            

            if keyboard.is_pressed(str(keyname)):
                print('Holding:', keyname)
                self.keyPresser.hold(vk_key)
                return 1
            else:
                print('Key pressed:', keyname)
                print('Pressing:', vk_key)
                self.keyPresser.press(vk_key)
                return 2


        Thread(target=code, args=(self, a)).start()
        # capture.forceMinimised() # Can cause issues. (Though you can have window minimised if you press btns a bunch)
        
        # time.sleep(1)

    # def keyReleased(self):
    #     pass


    def addText(self, img, TEXT, xy=(100,20), BGR=(0,0,255), thickness=1, fontScale=1):
        cv2.putText(img, TEXT, 
                    org=xy,
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=fontScale,
                    color=BGR,
                    thickness=thickness,
                    lineType=cv2.LINE_AA)


    def addCv2WindowInfo(self, frame, processTime, RGB=(255,0,0)):
        offset = 40

        fps = 1/(processTime-self.PREV_processTime)
        
        self.addText(frame, f'Window: {self.GAME_WINDOW_NAME} | {self.keyPresser.getHwnd()}', fontScale=1, BGR=RGB[::-1], xy=(10, offset), thickness=2)
        # addText(frame, f'Window Handle: {}', fontScale=1, BGR=RGB[::-1], xy=(10, offset*2))
        self.addText(frame, f'FPS: {fps}', fontScale=1, BGR=RGB[::-1], xy=(10, offset*2))

    def toggleCv2(self, setTo=None):
        '''Will either toggle it. Or you can set it with True/False with setTo'''
        if setTo:
            self.SHOWCV2WINDOW = setTo
        
        if self.SHOWCV2WINDOW:
            self.SHOWCV2WINDOW = False
        else:
            self.SHOWCV2WINDOW = True
        

    def start(self, showCV2Window=False, showFPS=False, FPSLabel=None, extraX=0, extraY=0, showAlertBoxes=True, exitKeyPressDetect=False, ignoreErrors=False):
        if self.EXITED:
            return
        

        self.SHOWCV2WINDOW = showCV2Window
        self.showFPS = showFPS

        self.ADDED_X_TO_SCREEN_CAPTURE = extraX
        self.ADDED_Y_TO_SCREEN_CAPTURE = extraY

        self.showAlertBoxes = showAlertBoxes


        if self.showAlertBoxes:
            messagebox.showinfo('WallpaperGaming', '(Run in command prompt to get verbose)')

        keyboard.on_press(callback=self.keyPressed)
        # keyboard.on_release(callback=self.keyReleased, suppress=suppressKeyPresses)

        while self.EXITED == False:
            st = time.time()
            try:
                img = self.capture.get_screenshot(addedX=self.ADDED_X_TO_SCREEN_CAPTURE, addedY=self.ADDED_Y_TO_SCREEN_CAPTURE)

                
                cv2.imwrite('screenshot.jpg', img)
                wallpaper2.set_wallpaper('screenshot.jpg')


                if exitKeyPressDetect:
                    if cv2.waitKey(1) == ord('q'):
                        print('Exit key pressed! Breaking...')
                        self.EXITED = True
                        break
                

                et = time.time()
                if self.SHOWCV2WINDOW:
                    self.addCv2WindowInfo(img, et-st, RGB=(0,255,0))
                    cv2.imshow("Capture", img)


                if self.showProcessTime:
                    print('Processing time:', et - st)
                if self.showFPS:
                    fps = round(1/((et-st)-self.PREV_processTime), 2)
                    print('FPS:', fps)
                    if FPSLabel:
                        try:
                            # Thread(target=FPSLabel.config, kwargs={"text": f"FPS: {fps}"}).start()
                            FPSLabel.config(text=f"FPS: {fps}")
                        except Exception as e:
                            if self.ignoreErrors:
                                continue
                            print('FPSLabel error:', e)
                            break
                    


                time.sleep(0.05)
                # time.sleep(0.1)


            except KeyboardInterrupt:
                if self.ignoreErrors:
                    continue
                print('Keyboard interrupt occurred! Breaking...')
                self.EXITED = True
                break
            except RuntimeError as e:
                if self.ignoreErrors:
                    continue
                if self.EXITED:
                    break
                else:
                    print('RuntimeError:', e)
            except Exception as e:
                if self.ignoreErrors:
                    continue
                print('Unknown error occurred! Breaking...')
                print('Error:', e)
                self.EXITED = True
                break


        print('Complete!')
        if self.showAlertBoxes:
            messagebox.showinfo('Wallpaper Gaming', 'Wallpaper Gaming : start(). Has finished!')
        # keyboard.on_release(callback=None)
    
    def exit(self, root:tk.Tk):
        
        self.EXITED = True
        try:
            cv2.destroyAllWindows()
        except:
            pass

        try:
            root.destroy()
        except:
            pass
        
        print('Resetting bg...')
        wallpaper2.set_wallpaper(self.BEFORE_BG)
        print('BG Reset.')

        print('Exited.')

        if self.showAlertBoxes:
            messagebox.showinfo('WallpaperGaming Closed')

        # sys.exit(0)