print("((BREAK BREAKER))\nMade by: Me")

import turtle
# import samples.keyPress as keyPress
# from keyManager import KeyEvent, KeyManager

class Vector:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y
        self.r = (x,y)

    @staticmethod
    def tuppleInit(r):
        x,y = r
        v = Vector(x,y)
        return v
        
    def __add__(self, v):
        return __class__(self.x + v.x, self.y + v.y)
    
    def __mul__(self, x):
        return __class__(x* self.x, x* self.y)
        
    def __str__(self):
        return str(self.r)

    def tupple(self):
        return self.x, self.y
    

class Ball:
    def __init__(self, vector, initialLocation):
        self.velocity = Vector(vector)
        self.location = Vector(initialLocation)
    
    def move(self):
        self.location += self.velocity

def rc():
    print("fuck you!")

import time
import datetime
import threading

class Game:
    gameObjects = []
    FRAMERATE = 1

    def __init__(self):
        super().__init__()
        self.InitializeUI()
        # self.Update()
        # t1 =threading.Thread(target=self.InitializeUI)
        
        t2 =threading.Thread(target=self.Update)
        # t1.start()
        # self.Update()

    def InitializeUI(self):

        self.ui = UI()

    @staticmethod
    def wait(secs):
        initialDate = datetime.datetime.now()
        delta = datetime.timedelta(seconds = secs)
        while True:
            now = datetime.datetime.now()
            if now - initialDate == delta:
                break

    @staticmethod
    def wwait(secs):
        t = 0 
        while t < secs:
            t+= 0.001
            time.sleep(0.001)

    def Update(self):
        
        thread = threading.Timer(1/Game.FRAMERATE, self.Update)

        for gameObject in self.gameObjects:
            gameObject.move()

        # Game.wait(1/Game.FRAMERATE)
        
    
        print("refresh")
        # thread.start()

def f():
    print("Fucl yuui'")

class UI:
    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 750
    def __init__(self):
        super().__init__()
        from turtle import Screen
        # self.window = Screen()
        self.window =Screen()

        win = self.window
        win.title("Another Brick Breaker Game :))")
        win.setup(UI.SCREEN_WIDTH*1.5, UI.SCREEN_HEIGHT*1.5) 
        win.screensize(canvwidth=UI.SCREEN_WIDTH, canvheight=UI.SCREEN_HEIGHT)     
        win.bgcolor("dark grey")
        # self.window.delay(0)  
        # self.window.onkey(f, "Right")
        self.arrow = Arrow()
        win.delay(1)
        # window.onkey(tiltLeft, "Left")
        self.setKeyEvents()
        win.listen()
        # win.exitonclick()
        win.mainloop()
        # input("Press Enter to Exit")
        # threading.Thread(target = KeyManager.start)


    def setKeyEvents(self):
        win = self.window
        win.onkeypress(self.arrow.tiltLeft, "Left")
        win.onkeypress(self.arrow.tiltRight, "Right")
        # win.onkeyrelease(self.arrow.stopTilting, "Left")
        # win.onkeyrelease(self.arrow.stopTilting, "Right")


class Direction:
    Left, Right, NONE = 0,1,2

# turtle.speed(10)
# turtle.delay(0)
# turtle.tracer(0, 0)
#no use =/

class Arrow:

    angV = 12 #angular velocity
    radius = 30
    angle = 0 #angle made from x axis
    tiltDirection = Direction.NONE
    # tilting = False
    tilter = None
    isTilting = False

    def __init__(self):
        super().__init__()
        self.turtle = turtle.Turtle()
        ted = self.turtle
        # print(ted.pos())
        # print("were goiongggg")
        radius = self.radius
        # ted.speed = 0
        ted.speed(0)
        # turtle.speed(0)
        ted.up()
        self.pivotPoint = ((0, (-1)*UI.SCREEN_HEIGHT/2))
        ted.goto(self.pivotPoint)
        ted.dot()
        ted.shape("arrow")
        # ted.shape("circle")
        ted.forward(radius)
        ted.resizemode("user")
        ted.shapesize(.5, 2,1)
        
    def tilt(self, dir= None):
        if dir == None:
            dir = self.tiltDirection
        from math import cos,sin, radians
        i = 1 if dir == Direction.Left else -1
        self.angle += i* self.angV
        ted = self.turtle
        teta = radians( self.angle )
        ted.goto( (Vector.tuppleInit(self.pivotPoint) + Vector(cos(teta), sin(teta))*self.radius).tupple() ) 
        ted.tilt(i* self.angV)

    def startTilting(self):     
        # if self.tilter == None:
        if not self.isTilting:
            self.isTilting = True
            while self.isTilting:
                self.tilter = threading.Timer(0.1, self.tilt) 
                self.tilter.start()

    def stopTilting(self):
        if self.tilter != None :
            self.tilter.cancel()
        if self.isTilting:
            self.isTilting = False
            print("stopping tilting ;/")

    def tiltLeft(self):
        self.tiltDirection = Direction.Left
        self.startTilting()

    def tiltRight(self):
        self.tiltDirection = Direction.Right
        self.startTilting()

class GameObject:
    location = Vector(0,0)
    velocity = Vector(0,0)
    
    def __init__(self, movable = False):
        self.movability = movable

    def move(self):
        self.location += self.velocity
    
# window.exitonclick()
Game()