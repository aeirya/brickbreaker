print("((BREAK BREAKER))\nMade by: Me")

import turtle

class Vector:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y
        self.r = (x,y)
        from math import sqrt, atan2
        self.size = sqrt(x**2+y**2)
        self.teta = atan2(y,x)

    @staticmethod
    def tuppleInit(r):
        x,y = r
        v = Vector(x,y)
        return v
    @staticmethod 
    def polarInit(r,t):
        v = Vector()
        v.size = r
        v.teta = t
        from math import cos,sin
        v.x = r*cos(t)
        v.y = r*sin(t)
        return v

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

        self.ui = UI()

        uiThread = threading.Timer(0.2, self.InitializeUI)
        uiThread.start()

        updateThread = threading.Timer(0.3, self.Update)
        updateThread.name = "Update Thread"
        updateThread.start()
        
    def InitializeUI(self):
        for _ in range(3):
            self.genBall()


    def genBall(self):
        print("generating a ball")
        import random
        startAngle = random.uniform(0,90)
        velocity = random.uniform(0,1)
        self.gameObjects.append(Ball( Vector.polarInit(velocity,startAngle).tupple() , (random.uniform(-25,25),0) ))

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

class UI:
    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 750
    deltaTime = 1/Game.FRAMERATE
    
    def __init__(self):
        super().__init__()
        from turtle import Screen
        self.window =Screen()
        win = self.window
        win.delay(1)

        win.bgcolor("dark grey")
        win.setup(0,0)
        win.title("Another Brick Breaker Game :))")
        self.arrow = Arrow()
        win.setup(UI.SCREEN_WIDTH*1.5, UI.SCREEN_HEIGHT*1.5) 
        win.screensize(canvwidth=UI.SCREEN_WIDTH, canvheight=UI.SCREEN_HEIGHT)
        self.setKeyEvents()
        win.listen()

        self.pen = turtle.Turtle()
        pen = self.pen
        pen.up()
        pen.speed(0)
        pen.hideturtle()

    updateTimerStacks = []

    def Update(self):
        self.deltaTime = (datetime.now() - self.lastCallTime).total_seconds()

        for gameObject in game.gameObjects:
            if gameObject != None:
                if gameObject.queue == False:
                    t = threading.Thread(target = gameObject.move)
                    t.name = "Turtle Move"
                    gameObject.queue = True
                    t.start()
                # gameObject.move()
        
        timer = threading.Timer(1/Game.FRAMERATE, self.Update)
        timer.name = "Next Update"

        self.lastCallTime = datetime.now()
        timer.start()

    def clear(self):
        win = self.window
        win.clear()
        win.bgcolor("dark grey")

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

    def __init__(self):
        super().__init__()
        self.pivotPoint = ((0, (-1)*UI.SCREEN_HEIGHT/2))
        self.turtle = turtle.Turtle()
        self.draw()

    def draw(self):
        ted = self.turtle
        radius = self.radius
        ted.speed(0)
        ted.up()
        ted.goto(self.pivotPoint)
        ted.dot()
        ted.shape("arrow")
        ted.forward(radius)
        ted.resizemode("user")
        ted.shapesize(.5, 2,1)   
    
    def tilt(self):
        i = self.tiltDirection
        if i == Direction.NONE:
            return
        from math import cos,sin, radians
        deltaTeta = i* self.angV * game.ui.deltaTime
        if 0 <= self.angle + deltaTeta <= 180:
            self.angle += deltaTeta
        else:
            # deltaTeta = 0
            return

        ted = self.turtle
        teta = radians( self.angle )
        ted.goto( (Vector.tuppleInit(self.pivotPoint) + Vector(cos(teta), sin(teta))*self.radius).tupple() ) 
        ted.tilt( deltaTeta )

        # if self.tilter!=None:
        #     self.tilter.cancel()
        self.tilter = threading.Timer(1/Game.FRAMERATE, self.tilt)
        self.tilter.name = "Tilt Timer"
        self.tilter.start()

    def startTilting(self):     
        if not self.isTilting:
            self.isTilting = True
            self.tilt()

    def stopTilting(self):
        if self.isTilting:
            if self.tilter != None :
                self.tilter.cancel()
            self.isTilting = False
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
        self.object.left(self.velocity.teta)

        self.queue = False
        # self.generator = game.ui.pen.clone()
        # pen = self.generator
        # pen.goto(initialLocation)

    def move(self):
        # self.location += self.velocity * game.ui.deltaTime
        pass
        # pen = self.generator
        # pen.clear()
        # pen.goto(self.location.tupple())

class Ball(GameObject):
    RADIUS = 10
    def __init__(self, vector = (0,0), initialLocation = (0,0)):
        super().__init__(vector, initialLocation)
        self.draw()
        
    def draw(self, fill = False):
        # ted.resizemode("user")
        # ted.shapesize(1, 1,0) 
        ted = self.object
        ted.turtlesize(0.7,0.7)
        ted.shape('circle')
        ted.up()

    def move(self):
        super().move()
        # self.object.tilt(30)
        # self.object.forward(10)
        self.object.forward(self.velocity.size)
        self.queue = False

game = Game()
print("Started Game ^^")

game.ui.window.mainloop()
