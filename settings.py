# -*- coding: utf-8 -*-

from appJar import gui
import _tkinter
import win32api
import json
import os

PATH = os.path.expanduser("~\\AppData\\Roaming\\PyKaomoji")
KLIST = None

def getSettings():
    with open(f"{PATH}\\config.json", encoding="utf-8") as fp:
        return json.load(fp)

def save():
    global KLIST
    settings = getSettings()
    settings["show"] = app.getEntry("Открыть/Скрыть overlay")
    settings["settings"] = app.getEntry("Открыть панель настроек")
    settings["left"] = app.getEntry("Overlay: шаг влево")
    settings["right"] = app.getEntry("Overlay: шаг вправо")
    settings["textcolor"] = app.getEntry("Цвет текста")
    settings["bgcolor"] = app.getEntry("Цвет заднего плана")
    settings["fgcolor"] = app.getEntry("Цвет переднего плана")
    settings["transparency"] = round(app.getEntry("Прозрачность (%)"))
    settings["data"] = KLIST
    
    with open(f"{PATH}\\config.json", "w", encoding="utf-8") as fw:
        json.dump(settings, fw, indent=4, ensure_ascii=False)

def drawRect():
    try:
        app.addCanvasRectangle("colors", 10, 5, 60, 10, fill=app.getEntry('Цвет заднего плана'))
        app.addCanvasRectangle("colors", 110, 5, 60, 10, fill=app.getEntry('Цвет переднего плана'))
        app.addCanvasRectangle("colors", 210, 5, 60, 10, fill=app.getEntry('Цвет текста'))
    except Exception:
        pass

def refresh():
    global KLIST

    KLIST = getSettings()["data"]
    app.replaceAllTableRows("klist", KLIST, deleteHeader=False)
    
    kcolor = getSettings()["textcolor"]
    bgcolor = getSettings()["bgcolor"]
    fgcolor = getSettings()["fgcolor"]

    for i in ['Горячие клавишы', 'Внешний вид', 'Каомодзи']:
        app.setLabelFrameBg(i, bgcolor)
        app.setLabelFrameFg(i, kcolor)

    app.addCanvasRectangle("colors", 10, 5, 60, 10, fill=fgcolor)
    app.addCanvasRectangle("colors", 110, 5, 60, 10, fill=bgcolor)
    app.addCanvasRectangle("colors", 210, 5, 60, 10, fill=kcolor)
    
    app.setBg(bgcolor)
    app.setFg(fgcolor)

    app.openSubWindow("Kaomoji management")
    app.setSize((win32api.GetSystemMetrics(0) - 50), (win32api.GetSystemMetrics(1) - (win32api.GetSystemMetrics(1) - (19 * len(KLIST)) - 50)))
    #app.setTableHeight("klist", (win32api.GetSystemMetrics(1) - (win32api.GetSystemMetrics(1) - (19 * len(KLIST)))))
    app.setBg(bgcolor)
    app.setFg(fgcolor)
    app.stopSubWindow()

    app.openLabelFrame("Каомодзи")
    app.setButtonBg("Управление каомодзи", fgcolor)
    app.stopLabelFrame()
    
    app.setButtonBg("Применить", fgcolor)
    app.setButtonFg("Применить", kcolor)

    for i in ['Открыть/Скрыть overlay', 'Открыть панель настроек', 'Overlay: шаг влево', 'Overlay: шаг вправо', 'Прозрачность (%)', 'Цвет заднего плана', 'Цвет переднего плана', 'Цвет текста']:
        app.setEntryBg(i, fgcolor)
        app.setEntryFg(i, kcolor)
        app.setEntryRelief(i, "groove")
        app.setEntryAnchor(i, "right")
        app.getEntryWidget(i).config(font="Courier")

        app.setEntry("Открыть/Скрыть overlay", getSettings()["show"])
        app.setEntry("Открыть панель настроек", getSettings()["settings"])
        app.setEntry("Overlay: шаг влево", getSettings()["left"])
        app.setEntry("Overlay: шаг вправо", getSettings()["right"])
        app.setEntry("Прозрачность (%)", getSettings()["transparency"])
        app.setEntry("Цвет заднего плана", getSettings()["bgcolor"])
        app.setEntry("Цвет переднего плана", getSettings()["fgcolor"])
        app.setEntry("Цвет текста", getSettings()["textcolor"])

def dmanagment():
    app.showSubWindow("Kaomoji management")

def kActions(action):
    global KLIST
    if action == "Сохранить и выйти":
        save()
        app.hideSubWindow("Kaomoji management")
    if action == "Выйти без сохранения":
        app.hideSubWindow("Kaomoji management")
    if action == "Удалить каомодзи":
        bl = app.getTableSelectedCells("klist")
        if bl != []:
            for i in bl:
                v1 = int(i[:i.find('-')])
                v2 = int(i[i.find('-') + 1:])
                try:
                    KLIST[v1][v2] = None
                except IndexError:
                    pass
            tmp = []
            newlist = []
            c = 0
            for i in KLIST:
                for j in i:
                    tmp.append(j)
                    
            while tmp.count(None) != 0:
                tmp.pop(tmp.index(None))

            if tmp != []:
                for i in range(len(tmp) // 12 + 1):
                    newlist.append([])
                    for j in range(12):
                        newlist[i].append(tmp[c])
                        c += 1
                        if c >= len(tmp):
                            break
            else:
                newlist = []

            KLIST = newlist

            app.replaceAllTableRows("klist", KLIST, deleteHeader=False)
            
    if action == "Добавить каомодзи":
        k = app.textBox("Добавление каомодзи", 'Введите каомодзи и нажмите "OK"', parent="Kaomoji management")
        tmp = []
        newlist = []
        c = 0
        for i in KLIST:
            for j in i:
                tmp.append(j)
        tmp.append(k)

        for i in range(len(tmp) // 12 + 1):
            newlist.append([])
            for j in range(12):
                newlist[i].append(tmp[c])
                c += 1
                if c >= len(tmp):
                    break

        KLIST = newlist

        app.replaceAllTableRows("klist", KLIST, deleteHeader=False)

try:
    with gui("PyKaomoji settings", showIcon = False) as app:
        app.winIcon = None
        app.setLocation("center")
        app.setSize('300x350')
        app.setResizable(False)
        app.setSticky("news")
        
        app.startLabelFrame("Горячие клавишы", 0, 0)
        app.setSticky("news")
        app.addLabelEntry("Открыть/Скрыть overlay")
        app.addLabelEntry("Открыть панель настроек")
        app.addLabelEntry("Overlay: шаг влево")
        app.addLabelEntry("Overlay: шаг вправо")
        app.stopLabelFrame()

        app.startLabelFrame("Внешний вид", 1, 0)
        app.setSticky("news")
        app.addNumericLabelEntry("Прозрачность (%)")
        app.addLabelEntry("Цвет заднего плана")
        app.addLabelEntry("Цвет переднего плана")
        app.addLabelEntry("Цвет текста")
        app.addCanvas("colors")
        app.setCanvasWidth('colors', 50)
        app.setCanvasHeight('colors', 25)
        app.stopLabelFrame()

        app.startLabelFrame("Каомодзи", 2, 0)
        app.setSticky("news")
        app.addButton("Управление каомодзи", dmanagment)
        app.setButtonRelief("Управление каомодзи", "groove")
        app.stopLabelFrame()

        app.addButton("Применить", save)
        app.setButtonRelief("Применить", "groove")

        app.setEntryChangeFunction('Цвет заднего плана', drawRect)
        app.setEntryChangeFunction('Цвет переднего плана', drawRect)
        app.setEntryChangeFunction('Цвет текста', drawRect)

        app.startSubWindow("Kaomoji management", modal=True)
        app.setIcon(f"{PATH}\\logo.ico")
        app.hideTitleBar()
        app.setLocation(25, 10)
        app.setResizable(False)
        app.setSticky("news")
        app.addTable("klist", [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="]])
        app.addButtons(["Добавить каомодзи", "Удалить каомодзи", "Сохранить и выйти", "Выйти без сохранения"], kActions)
        app.stopSubWindow()

        app.setIcon(f"{PATH}\\logo.ico")

        refresh()

        app.go()

except _tkinter.TclError:
    pass
