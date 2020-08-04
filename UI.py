# -*- coding: utf-8 -*-

from appJar import gui
from time import sleep
import threading
import keyboard
import win32api
import win32gui
import win32con
import shutil
import json
import os

HIDDEN = False
SHIFT = 0
PATH = os.path.expanduser("~\\AppData\\Roaming\\PyKaomoji")

def getSettings():
    global PATH
    with open(f"{PATH}\\config.json", encoding="utf-8") as fp:
        return json.load(fp)

def preInit():
    global PATH
    data = {
        "show": "ctrl+k",
        "settings": "ctrl+i",
        "left": "ctrl+-",
        "right": "ctrl+=",
        "rows": 1,
        "textcolor": "#000000",
        "bgcolor": "#CFCFCF",
        "fgcolor": "#A0A0A0",
        "transparency": 70,
        "switchfix": True,
        "data": [
            [
                "(* ^ ω ^)",
                "(´ ∀ ` *)",
                "٩(◕‿◕｡)۶",
                "☆*:.｡.o(≧▽≦)o.｡.:*☆",
                "(o^▽^o)",
                "(⌒▽⌒)☆",
                "<(￣︶￣)>",
                "。.:☆*:･'(*⌒―⌒*)))",
                "ヽ(・∀・)ﾉ",
                "(´｡• ω •｡`)",
                "(￣ω￣)",
                "｀;:゛;｀;･(°ε° )"
            ],
            [
                "(o･ω･o)",
                "(＠＾◡＾)",
                "ヽ(*・ω・)ﾉ",
                "(o_ _)ﾉ彡☆",
                "(^人^)",
                "(o´▽`o)",
                "(*´▽`*)",
                "｡ﾟ( ﾟ^∀^ﾟ)ﾟ｡"
            ]
        ]
    }
    
    os.mkdir(PATH)
    shutil.copyfile(f'{os.path.dirname(os.path.realpath(__file__))}\\logo.ico' , f"{PATH}\\logo.ico")
    with open(f"{PATH}\\config.json", "w", encoding="utf-8") as fw:
        json.dump(data, fw, indent=4, ensure_ascii=False)
        

def init():
    def topmost(hw):
        while True:
            win32gui.BringWindowToTop(hw)

    def permaKeys():
        keyboard.add_hotkey(getSettings()["settings"], callSettings, suppress=False)
        keyboard.add_hotkey(getSettings()["show"], toggle, suppress=False)

    def setControls():
        keyboard.add_hotkey(getSettings()["left"], build, suppress=False, args=['left'])
        keyboard.add_hotkey(getSettings()["right"], build, suppress=False, args=['right'])

    def send(text):
        keyboard.press("backspace")
        keyboard.write(text)

    def build(*direction):
        global SHIFT
        #if getSettings()["switchfix"]:
        #    keyboard.press("backspace")
        kcolor = getSettings()["textcolor"]
        bgcolor = getSettings()["bgcolor"]
        fgcolor = getSettings()["fgcolor"]
        app.setTransparency(getSettings()["transparency"])
        keys = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        keynames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="]
        ramount = getSettings()["rows"]
        camount = 12
        pady = 10
        size = (win32api.GetSystemMetrics(0) - 50), (win32api.GetSystemMetrics(1) - (win32api.GetSystemMetrics(1) - (50 * ramount) - pady))
        step = (size[0] - 50) // camount
        padx = (size[0] - (step * 12)) // 2
        app.clearCanvas("main")
        app.setSize(size)
        app.setBg(bgcolor)

        pos = padx + step - (step // 2) - 3
        for i in keynames:
            app.addCanvasText("main", pos, 6, i, fill=fgcolor, font=("Arial Black", 12))
            pos += step
            
        for i in range(ramount):
            pos = padx + step - 3
            for j in range(camount - 1):
                app.addCanvasLine("main", pos, (50 * i + pady + 3), pos, (50 * i + pady + 45), width=3, fill=fgcolor)
                pos += step

        if direction != ():
            keyboard.unhook_all_hotkeys()
            setControls()
            permaKeys()
            direction = direction[0]
        if direction == "left":
            SHIFT -= 1
        if direction == "right":
            SHIFT += 1

        kdata = getSettings()["data"]
        while len(kdata) % ramount != 0:
            kdata.append([])

        if SHIFT * ramount >= len(kdata):
            SHIFT = 0
        if SHIFT < 0:
            SHIFT = len(kdata) - ramount
            
        pady = 33
        for i in range(ramount):
            index = 0
            pos = padx + step - (step // 2) - 3
            for j in kdata[i + SHIFT]:
                app.addCanvasText("main", pos, (50 * i + pady), j, fill=kcolor, font=("Calibri", 12))
                keyboard.add_hotkey(keys[index], send, suppress=False, args=[j])
                pos += step
                index += 1

    def toggle():
        global HIDDEN
        if HIDDEN:
            app.show()
            setControls()
            build()
        else:
            app.hide()
            keyboard.unhook_all_hotkeys()
            permaKeys()
        HIDDEN = not(HIDDEN)

    def callSettings():
        os.startfile(f'{os.path.dirname(os.path.realpath(__file__))}\\settings.exe')

    def winSettings(name):
        hw = win32gui.FindWindow(None, name)
        win32gui.SetWindowLong(hw, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hw, win32con.GWL_EXSTYLE) | win32con.WS_EX_PALETTEWINDOW | win32con.WS_EX_TRANSPARENT)
        threading.Thread(target=topmost, args = [hw]).start()

    app.addCanvas("main")
    build()
    toggle()
    winSettings("PyKaomoji")

with gui("PyKaomoji", showIcon = False) as app:
    app.winIcon = None
    app.hideTitleBar()
    app.setLocation(25, 10)
    app.setSticky("news")
    if os.path.isdir(PATH) == False:
        preInit()
    app.setIcon(f"{PATH}\\logo.ico")
    app.go(init())
