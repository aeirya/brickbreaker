print("((BREAK BREAKER))\nMade by: Me")

class Vector:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y
        self.r = (x,y)
        
    def __add__(self, v):
        return __class__(self.x + v.x, self.y + v.y)
    
    def __str__(self):
        return str(self.r)

class Ball:
    def __init__(self, vector, initialLocation):
        self.velocity = Vector(vector)
        self.location = Vector(initialLocation)
    
    def move(self):
        self.location += self.velocity


import tkinter
# from PIL import ImageTk, Image
from tkinter import Image
tkinter.PhotoImage
class Arrow():
    def __init__(self,window,x):
        img = Image.open('arrow.png')
        arrowImg = ImageTk.PhotoImage(img)
        arrow = x.Label(window, image = arrowImg)
        arrow.grid(row = 2, column=2)

def readyInterface():
    from tkinter import ttk as x
    window = tkinter.Tk()
    # x = tkinter.ttk
    arrow = Arrow(window,x)
    
    # quit_button = x.Button(window, text="Quit")
    # quit_button.grid(row=2, column=1)
    return window

def readyEvents(window):
    pass

def Start():
    window = readyInterface()
    readyEvents(window)
    window.mainloop()

# def Update():
#     pass

Start()

