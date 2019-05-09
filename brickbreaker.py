print("((BREAK BREAKER))\nMade by: Me")

import turtle
import samples.keyPress as keyPress

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
        # window.onkey(tiltLeft, "Left")
        self.setKeyEvents()
        win.listen()
        win.exitonclick()
        # input("Press Enter to Exit")

    def setKeyEvents(self):
        win = self.window
        win.onkey(self.arrow.tiltLeft, "Left")
        win.onkey(self.arrow.tiltRight, "Right")
        # win.on

class Direction:
    Left, Right = 0,1

# turtle.speed(10)
# turtle.delay(0)
# turtle.tracer(0, 0)
#no use =/

class Arrow:

    angV = 12 #angular velocity
    radius = 30
    angle = 0 #angle made from x axis
    
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

    def tilt(self, dir):
        from math import cos,sin, radians
        i = 1 if dir == Direction.Left else -1
        self.angle += i* self.angV
        ted = self.turtle
        teta = radians( self.angle )
        ted.goto( (Vector.tuppleInit(self.pivotPoint) + Vector(cos(teta), sin(teta))*self.radius).tupple() ) 
        ted.tilt(i* self.angV)

    def tiltLeft(self):
        self.tilt(Direction.Left)

    def tiltRight(self):
        self.tilt(Direction.Right)

class GameObject:
    location = Vector(0,0)
    velocity = Vector(0,0)
    
    def __init__(self, movable = False):
        self.movability = movable

    def move(self):
        self.location += self.velocity
    
# window.exitonclick()
Game()