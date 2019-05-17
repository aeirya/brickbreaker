print("((BREAK BREAKER))\nMade by: Me")

import turtle

class Vector:
    def __init__(self, x=(0,0) ,y=None):
        if y == None:
            x,y = x
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

    @staticmethod
    def i(t):
        return Vector.polarInit(1,t)

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
    balls = []
    bricks = []
    FRAMERATE = 30
    
    def __init__(self):
        super().__init__()

        self.ui = UI(self)
        self.setKeys()
        uiThread = threading.Timer(0.2, self.InitializeUI)
        uiThread.start()
        
        physics = Physics()
        updateThread = threading.Timer(0.3, self.Update)
        updateThread.name = "Update Thread"
        updateThread.start()
        
    def InitializeUI(self):
        # gen balls and bricks
        # for i in range(3):
        #     self.genBall()
        # Rect((UI.SCREEN_WIDTH*0.6,30), 90, (1,50))
        # Rect((UI.SCREEN_WIDTH*0.6*(-1),30), 90, (1,50))
        # a=Brick( (0,0))
        b=Brick( (0,150))
        # game.gameObjects.append(a)
        self.bricks.append(b)
        
        # self.gameObjects += self.bricks + self.balls

    def genBall(self):
        print("generating a ball")
        import random
        startAngle = random.uniform(-90,90)
        velocity = random.uniform(0,5)
        self.balls.append(Ball( Vector.polarInit(velocity,startAngle).tupple() , (random.uniform(-25,25),0) ))

    # def genBrick(self):

    def setKeys(self):
        # self.ui.window.onkeypress(self.Quit(), "w")
        pass

    def shoot(self):
        # print("Pew!")
        arrow = self.ui.arrow
        direction = Vector.i(arrow.angle)
        initPos = Vector(tuple(arrow.turtle.pos())) + direction*(Ball.RADIUS*3 + arrow.length)
        # print(type(initPos))
        for i in range(5):
            self.balls.append( Ball( initPos, direction ) ) 
            time.sleep(0.005)

    @staticmethod
    def wait(secs):
        initialDate = datetime.datetime.now()
        delta = datetime.timedelta(seconds = secs)
        while True:
            now = datetime.datetime.now()
            if now - initialDate == delta:
                break

    def Update(self):
        self.ui.lastCallTime = datetime.now()
        self.ui.Update()

    def Quit(self):
        print("BYE!")
        self.ui.window.bye()
        quit(0)

class Physics:
    
    def __init__(self):
        print(super())

    @staticmethod
    def move():
        pass
    
    @staticmethod
    def checkCollision(ball, rect):
        pass

class UI:
    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600
    deltaTime = 1/Game.FRAMERATE
    
    def __init__(self, game):
        super().__init__()

        self.game = game

        from turtle import Screen
        self.window =Screen()
        win = self.window
        win.tracer(0,0) 
        win.bgcolor("dark grey")
        win.setup(0,0)
        win.title("Another Brick Breaker Game :))")
        self.arrow = Arrow()
        self.game.gameObjects.append(self.arrow)
        win.setup(UI.SCREEN_WIDTH*1.5, UI.SCREEN_HEIGHT*2) 
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
        return (datetime.now() - self.lastCallTime).total_seconds()

    def Update(self):
        self.deltaTime = self.DeltaTime()
        self.lastCallTime = datetime.now()
        self.gameObjects = [self.arrow] + self.game.balls + self.game.bricks
        for obj in self.gameObjects:
            if obj != None:
                t = threading.Thread(target = obj.refresh)
                t.name = "Object Refresh"
                self.threads.append(t)
                t.start()
        
        # Physics.checkCollision( 

        for t in self.threads:
            while t.isAlive():
                time.sleep(1/Game.FRAMERATE/10)

        x = 1/Game.FRAMERATE - self.DeltaTime()
        if x > 0 : time.sleep(x)
        self.window.update()
        self.Update()

    def setKeyEvents(self):
        win = self.window
        win.onkeypress(self.arrow.tiltLeft, "Left")
        win.onkeypress(self.arrow.tiltRight, "Right")
        win.onkeyrelease(self.arrow.stopTilting, "Left")
        win.onkeyrelease(self.arrow.stopTilting, "Right")
        win.onkeypress(self.game.shoot, "space")

class Direction:
    Left, Right, NONE = 1,-1,0

class Arrow:
    radius = 30
    angle = 0 #angle made from x axis
    tiltDirection = Direction.NONE
    tilter = None
    isTilting = False
    angV = 3 * Game.FRAMERATE
    length = 2
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
        ted.shapesize(self.length*0.2, self.length,1)   
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

    Points = [] * 4

    def __init__(self, initialLocation=Vector(0,0), vector= Vector(0,0) ):
        if type(initialLocation) == type(tuple()):
            self.location = Vector.tuppleInit(initialLocation)
        else:
            self.location = initialLocation

        self.object = turtle.Turtle()
        self.object.hideturtle()
        self.object.up()
        self.object.goto(self.location.tupple())
        self.object.left(vector.angle())


class Ball(GameObject):
    RADIUS = 10
    speed = 10 * Game.FRAMERATE

    def __init__(self, initialLocation = (0,0), vector = Vector(0,0) ):
        super().__init__(initialLocation, vector )
        # self.velocity = Vector.tuppleInit(vector) * Game.FRAMERATE
        self.velocity = vector * self.speed
        self.draw()
        
    def draw(self, fill = False):
        ted = self.object
        ted.turtlesize(0.7,0.7)
        ted.shape("circle")
        ted.up()
        ted.showturtle()
    
    def refresh(self):
        self.move()

    def move(self):
        self.object.forward(self.speed * game.ui.deltaTime)

class Rect(GameObject):
    def __init__(self, initialLocation, angle,size):
        super().__init__(initialLocation, Vector.i(angle))
        # pen = self.object
        # pen.shape("square")
        self.size = size
        # pen.turtlesize(w,l)
        # pen.showturtle()
        self.draw()
        

    def draw(self):
        pen = self.object
        center = Vector(pen.pos()[0], pen.pos()[1])
        w,l = self.size
        Points = [ Vector( w/2, -l/2 ), Vector( -w/2, -l/2 ),
         Vector( -w/2, l/2 ) , Vector ( w/2, l/2 ) ]
        for i in range(len(Points)):
            Points[i] += center

        # pen.speed(0)
        pen.forward(w/2)
        pen.down()
        pen.fillcolor('brown')
        pen.begin_fill()
        pen.pensize(3)

        for p in Points:
            pen.goto(p.tupple())

        pen.goto(Points[0].tupple())

        pen.end_fill()

        self.Points = Points


class Brick(Rect):
    angle = 0
    # size = 5,2.5
    size = UI.SCREEN_WIDTH/6, UI.SCREEN_HEIGHT/9

    def __init__(self, initialLocation ):
        super().__init__(initialLocation, self.angle, self.size)

    def refresh(self):
        pass
        #update health
        #show health / destroy

class Wall(Rect):
    pass

game = Game()
print("Started Game ^^")
game.ui.window.mainloop()
