# from brickbreaker import Direction
from vector import Vector

from gamemanager import GameManager as gm
from gamemanager import UI

import turtle
from turtle import Vec2D

class Direction:
    Left, Right, NONE = 1,-1,0

class Arrow:
    RADIUS : int = 30 
    angle = 0 #angle made from x axis
    tiltDirection = Direction.NONE
    tilter = None
    isTilting = False
    length = 2
    T = 0

    def __init__(self):
        super().__init__()

        # from brickbreaker import UI
        import turtle
        self.angV = gm.ARROW_VELOCITY * gm.FRAMERATE

        self.pivotPoint = ((0, (-1)*UI.SCREEN_HEIGHT/2))
        self.turtle = turtle.Turtle()
        self.draw()

    def draw(self):
        ted = self.turtle
        radius = self.RADIUS
        ted.speed(0)
        ted.up()
        ted.goto(self.pivotPoint)
        ted.dot()
        ted.shape("arrow")
        ted.forward(radius)
        ted.resizemode("user")
        ted.shapesize(self.length*0.2, self.length,1)   
        
    def refresh(self, deltaTime):
        self.tilt(deltaTime)
        # print(self.T)

    def tilt(self, deltaTime):
        i = self.tiltDirection
        if i == Direction.NONE: return

        from math import cos,sin
        deltaTeta = i* self.angV * deltaTime

        if not 0 <= self.angle + deltaTeta <= 180:
            return
        self.angle += deltaTeta

        ted = self.turtle
        ted.goto( (Vector.tuppleInit(self.pivotPoint) + Vector.polarInit(self.RADIUS, self.angle)).tupple() ) 
        ted.tilt( deltaTeta )

    # def startTilting(self):     
    #     self.T += self.tiltDirection

        # x = self.T
        # if abs(x)>1:
        #     self.T = abs(x)/x

    def stopTilting(self):
        # if self.T != 0:
        self.tiltDirection = Direction.NONE

    def tiltLeft(self):
        self.tiltDirection = Direction.Left
        # self.startTilting()

    def tiltRight(self):
        self.tiltDirection = Direction.Right
        # self.startTilting()

class GameObject:

    Points = [] * 4

    def __init__(self, initialLocation=Vec2D(0,0), vector= Vector(0,0) ):
        if type(initialLocation) == type(tuple()):
            self.location = Vector(initialLocation).toVec2D()
        else:
            self.location = initialLocation
        
        # self.object = turtle.Turtle()
        # self.object.up()


        global turtleInstance
        # self.object.goto(self.location.tupple())
        # print( turtleInstance.position())
        # print(self.location)
        if turtleInstance.position() != self.location:
            turtleInstance.goto(self.location)
            # print("going")
        self.object = turtleInstance.clone()
        # turtle

        # self.object.hideturtle()
        # self.object.left(vector.angle())


class Ball(GameObject):
    # RADIUS = 10
    RADIUS = gm.BALL_RADIUS
    # speed = 10 #* FRAMERATE
    speed = gm.BALL_VELOCITY * gm.FRAMERATE

    def __init__(self, initialLocation = Vec2D(0,0), vector = Vector(0,0), t : int = 0):
        super().__init__(initialLocation, vector )
        
        self.draw()
        self.velocity = vector * self.speed

        # self.object

        self.object.left(vector.angle())
        if t!=0:
            self.object.hideturtle()
        self.t = t
        
    def draw(self, fill = False):
        ted = self.object
        # ted.turtlesize(0.7,0.7)
        # ted.pensize(2)

        # ted.shape("circle")
        # ted.up()
        # ted.down()
        ted.shape(UI.soccerball)
        ted.showturtle()
    
    def refresh(self, deltaTime):
        if self.t > 0: 
            self.t-= deltaTime
            if self.t <= 0:
                self.object.showturtle()
        # print(self.t)
        if self.t <= 0: self.move(deltaTime)

    def move(self, deltaTime):
        # fill = True
        # self.object.clear()
        # if fill: self.object.begin_fill()
        self.object.forward(self.speed * deltaTime)
        # self.object.circle(self.RADIUS)
        # if fill: self.object.end_fill()
        
    def checkCollision( rect ):
        pass

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
    size = 5,2.5
    

    def __init__(self, initialLocation = Vector(0,0) ):
        super().__init__(initialLocation, self.angle, self.size)
        self.size = UI.SCREEN_WIDTH/6, UI.SCREEN_HEIGHT/9

    def refresh(self):
        pass
        #update health
        #show health / destroy

class Wall(Rect):
    pass


turtleInstance = turtle.Turtle()
turtleInstance.hideturtle()
turtleInstance.up()