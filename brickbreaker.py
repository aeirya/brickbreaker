print("((BREAK BREAKER))\nMade by: Me")

import turtle

class Vector:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y
        
    def r(self):
        return (self.x, self.y)

    def size(self):
        from math import sqrt
        return sqrt(self.x**2 + self.y**2)

    def angle(self):
        from math import atan2, degrees
        return degrees(atan2(self.y, self.x))

    @staticmethod
    def tuppleInit(r):
        x,y = r
        return Vector(x,y)

    @staticmethod 
    def polarInit(r,t):
        from math import cos,sin,radians
        t = radians(t)
        return Vector(r*cos(t), r*sin(t))

    def __add__(self, v):
        return __class__(self.x + v.x, self.y + v.y)
    
    def __mul__(self, x):
        return __class__(x* self.x, x* self.y)
        
    def __str__(self):
        return str(self.r)

    def tupple(self):
        return self.x, self.y

import time
from datetime import datetime, timedelta
import threading

class Game:
    gameObjects = []
    FRAMERATE = 30
    
    def __init__(self):
        super().__init__()

        self.ui = UI(self)
        self.setKeys()
        uiThread = threading.Timer(0.2, self.InitializeUI)
        uiThread.start()

        updateThread = threading.Timer(0.3, self.Update)
        updateThread.name = "Update Thread"
        updateThread.start()
        
    def InitializeUI(self):
        # gen balls and bricks

        Brick((UI.SCREEN_WIDTH*0.6,30), 90, 50)
        Brick((UI.SCREEN_WIDTH*0.6*(-1),30), 90, 50)
        
    def genBall(self):
        print("generating a ball")
        import random
        startAngle = random.uniform(0,90)
        velocity = random.uniform(0,1)
        self.gameObjects.append(Ball( Vector.polarInit(velocity,startAngle).tupple() , (random.uniform(-25,25),0) ))

    def setKeys(self):
        # self.ui.window.onkeypress(self.Quit(), "w")
        pass

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
        self.ui.lastCallTime = datetime.now()
        self.ui.Update()

    def Quit(self):
        print("BYE!")
        self.ui.window.bye()
        quit(0)

class UI:
    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 700
    deltaTime = 1/Game.FRAMERATE
    
    def __init__(self, game):
        super().__init__()

        self.game = game

        from turtle import Screen
        self.window =Screen()
        win = self.window
        win.tracer(0,0) 
        win.bgcolor("light grey")
        win.setup(0,0)
        win.title("Another Brick Breaker Game :))")
        self.arrow = Arrow()
        self.game.gameObjects.append(self.arrow)
        win.setup(UI.SCREEN_WIDTH*1.5, UI.SCREEN_HEIGHT*1.5) 
        win.screensize(canvwidth=UI.SCREEN_WIDTH, canvheight=UI.SCREEN_HEIGHT)
        self.setKeyEvents()
        win.listen()

        self.pen = turtle.Turtle()
        pen = self.pen
        pen.up()
        pen.speed(0)
        pen.hideturtle()

    threads = []
    
    def DeltaTime(self):
        # if self.lastCallTime == None: return datetime.now()
        return (datetime.now() - self.lastCallTime).total_seconds()

    def Update(self, frame=0):
        self.deltaTime = self.DeltaTime()
        # print(self.deltaTime)
        print(frame)
        self.lastCallTime = datetime.now()

        for obj in self.game.gameObjects:
            if obj != None:
                t = threading.Thread(target = obj.refresh)
                t.name = "Object Refresh"
                self.threads.append(t)
                t.start()
        
        # time.sleep(1/Game.FRAMERATE - self.DeltaTime())
        self.window.update()
        # self.Update(frame+1)
        threading.Timer(1/Game.FRAMERATE, self.Update()).start()


    def setKeyEvents(self):
        win = self.window
        win.onkeypress(self.arrow.tiltLeft, "Left")
        win.onkeypress(self.arrow.tiltRight, "Right")
        win.onkeyrelease(self.arrow.stopTilting, "Left")
        win.onkeyrelease(self.arrow.stopTilting, "Right")

class Direction:
    Left, Right, NONE = 1,-1,0

class Arrow:
    radius = 30
    angle = 0 #angle made from x axis
    tiltDirection = Direction.NONE
    tilter = None
    isTilting = False
    angV = 3 * Game.FRAMERATE
    T = 0

    def __init__(self):
        super().__init__()
        self.pivotPoint = ((0, (-1)*UI.SCREEN_HEIGHT/2))
        self.turtle = turtle.Turtle()
        self.draw()

    def draw(self):
        ted = self.turtle
        # ted.hideturtle()
        radius = self.radius
        ted.speed(0)
        ted.up()
        ted.goto(self.pivotPoint)
        ted.dot()
        ted.shape("arrow")
        ted.forward(radius)
        ted.resizemode("user")
        ted.shapesize(.5, 2,1)   
        # ted.stamp()
        
    def refresh(self):
        self.tilt()

    def tilt(self):
        i = self.tiltDirection
        if i == Direction.NONE: return

        from math import cos,sin
        deltaTeta = i* self.angV * game.ui.deltaTime

        if not 0 <= self.angle + deltaTeta <= 180:
            return
        self.angle += deltaTeta

        ted = self.turtle
        ted.goto( (Vector.tuppleInit(self.pivotPoint) + Vector.polarInit(self.radius, self.angle)).tupple() ) 
        ted.tilt( deltaTeta )

    def startTilting(self):     
        self.T += self.tiltDirection

    def stopTilting(self):
        if self.T != 0:
            self.tiltDirection = Direction.NONE

    def tiltLeft(self):
        self.tiltDirection = Direction.Left
        self.startTilting()

    def tiltRight(self):
        self.tiltDirection = Direction.Right
        self.startTilting()

class GameObject:
    def __init__(self, vector= (0,0), initialLocation=(0,0), movable = False):
        self.movability = movable
        self.velocity = Vector.tuppleInit(vector) * Game.FRAMERATE
        self.location = Vector.tuppleInit(initialLocation)

        self.object = turtle.Turtle()
        self.object.hideturtle()
        self.object.up()
        self.object.goto(initialLocation)
        # self.object.left(self.velocity.teta)
        from math import degrees
        self.object.tilt(self.velocity.angle())
        self.queue = False

    def refresh(self):
        self.move()

    def move(self):
        pass

class Ball(GameObject):
    RADIUS = 10
    def __init__(self, vector = (0,0), initialLocation = (0,0)):
        super().__init__(vector, initialLocation)
        self.draw()
        
    def draw(self, fill = False):
        ted = self.object
        ted.turtlesize(0.7,0.7)
        ted.shape('circle')
        ted.up()
        ted.showturtle()
    
    def move(self):
        super().move()
        self.object.forward(self.velocity.size* game.ui.deltaTime)
        self.queue = False

class Brick(GameObject):
    def __init__(self, initialLocation, angle,size):
        super().__init__(Vector.polarInit(size,angle).tupple(), initialLocation)
        pen = self.object
        pen.shape("square")
        pen.turtlesize(1,size)
        pen.showturtle()

game = Game()
print("Started Game ^^")
game.ui.window.mainloop()
