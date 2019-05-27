# from brickbreaker import Direction
from vector import Vector

from gamemanager import GameManager as gm
from gamemanager import UI, Shape

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

        self.pivotPoint = ((0, (-1)*UI.SCREEN_HEIGHT * (0.75+0.5)/2))
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

        global turtleInstance
        if turtleInstance.position() != self.location:
            turtleInstance.goto(self.location)
        self.object = turtleInstance.clone()

class Ball(GameObject):
    # RADIUS = 10
    RADIUS = gm.BALL_RADIUS
    # speed = 10 #* FRAMERATE
    speed = gm.BALL_VELOCITY * gm.FRAMERATE

    def __init__(self, initialLocation = Vec2D(0,0), vector = Vector(0,0), t : int = 0):
        super().__init__(initialLocation, vector )
        
        self.draw()
        self.changeDirection(vector)

        self.object.left(vector.angle())
        if t!=0:
            self.object.hideturtle()
        self.t = t

    def changeDirection(self, vector):
        self.direction = vector
        self.velocity = vector * self.speed

    def generatePoints(self):
        r = self.RADIUS
        points = [ (-r,0), (r,0), (0,r) , (0,-r) ]
        for i in range(len(points)):
            points[i] += self.location
        
        
    def draw(self, fill = False):
        ted = self.object
        ted.shape(Shape.soccerball)
        ted.showturtle()
    
    def refresh(self, deltaTime):
        if self.t > 0: 
            self.t-= deltaTime
            if self.t <= 0:
                self.object.showturtle()
        if self.t <= 0: 
            self.move(deltaTime)
            # self.Points = self.generatePoints()

    def move(self, deltaTime):
        # self.object.forward(self.speed * deltaTime)
        displacement = (self.velocity * deltaTime).toVec2D()
        self.location += displacement
        self.object.goto( self.location )
        
    def checkCollision(self, rect ):
        # print(self.object.pos())
        collision = False
        d = self.direction
        p = rect.Points
        if p[0].y < d.y < p[1].y:
            if d.x > 0 :
                #check brick from left
                pass

        b,a = p[1],p[2]
        
        print(a.x,b.x, self.object.pos()[0])

        if a.x < d.x < b.x:
            if d.y > 0: #check from bottom
                # print("yaaaay")
                if abs( self.object.pos()[1] + self.velocity.y * 1/gm.FRAMERATE - p[-1].y ) <= self.RADIUS + rect.size[1]/2:
                    self.changeDirection( Vector(d.x , -d.y) )
                    collision = True
                    # print("changing direciton")
        return collision

class Rect(GameObject):
    def __init__(self, initialLocation ,size):
        super().__init__(initialLocation)
        self.size = size
        self.draw()
      

    def draw(self):
        pen = self.object
        center = Vector(pen.pos()[0], pen.pos()[1])
        w,l = self.size
        Points = [ (w,l) , (w,-l) , (-w,-l) , (-w,l), (0,0) ]
        for i,v in enumerate(Points):
            Points[i] = Vector(v)/2 + center

        # pen.speed(0)
        pen.forward(w/2)
        pen.down()
        pen.fillcolor('brown')
        pen.begin_fill()
        pen.pensize(3)

        for p in Points[:-1]:
            pen.goto(p.tupple())

        pen.goto(Points[0].tupple())

        pen.end_fill() 
        pen.up()
        pen.goto(center.toVec2D() + (-5,-10))
        self.Points = Points


class Brick(Rect):

    size = UI.SCREEN_WIDTH/6, UI.SCREEN_HEIGHT/9
    health = 0
    isDamaged = True

    def __init__(self, initialLocation = Vec2D(0,0) ):  
        super().__init__(initialLocation, self.size)
        self.spawn(1)

    def refresh(self):
        if self.isDamaged:
            hFont = ('Arial', 22)
            if self.health != 0:
                self.object.undo()
                self.object.write(self.health, font = (hFont) )
                self.isDamaged = False
            else:
                self.object.clear()
        #update health
        #show health / destroy

    def spawn(self, intitHealth):
        self.health = intitHealth
        self.object.dot()

class Wall(Rect):
    pass

turtleInstance = turtle.Turtle()
turtleInstance.hideturtle()
turtleInstance.up()
