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
from tkinter import ttk
# from tkinter import Image

class Arrow():
    def __init__(self,window):
        photo = tkinter.PhotoImage(file = "arrow.png")
        arrow = tkinter.ttk.Label(window, image = photo)
        label = tkinter.ttk.Label(image=photo)
        label.image = photo # keep a reference!
        label.grid(row = 2, column=2)
        label.pack()

def readyInterface():
    window = tkinter.Tk()
    arrow = Arrow(window)
    ``
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

