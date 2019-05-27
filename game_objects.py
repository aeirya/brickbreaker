# from brickbreaker import Direction
from vector import Vector

from gamemanager import GameManager as gm
from gamemanager import UI, Shape

import turtle
from turtle import Vec2D

class Direction:
    Left, Right, NONE = 1,-1,0
    Horizontal, Vertical = "y", "x"

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

        # self.object.left(vector.angle())
        if t!=0:
            self.object.hideturtle()
        self.t = t

    def changeDirection(self, vector):
        self.direction = vector
        self.velocity = vector * self.speed

    # def generatePoints(self):
    #     r = self.RADIUS
    #     points = [ (-r,0), (r,0), (0,r) , (0,-r) ]
    #     for i in range(len(points)):
    #         points[i] += self.location
        
    def draw(self, fill = False):
        ted = self.object
        ted.shape(Shape.soccerball)

        ted.showturtle()
        # ted.down() #
    
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

    def collides(self, rect ):
        p = rect.Points
        direction = self.direction
        displacement =  self.velocity / gm.FRAMERATE
        # displacement = Vector(0,0)
        location = Vector(self.location)
        size = Vector(rect.size)

        def calc(p1,p2, radius, location, displacement, size, direction):
            
            f = lambda a : a.getX()
            g = lambda a : a.getY()

            if direction == Direction.Vertical: 
                f,g = g,f
                
            # print( f(p1),f(location), f(p2), "is it true?")
            # print(f(location))
            if f(p1) <= f(location) <= f(p2):
                # print("TRUE")
                # print(radius - abs( g(location) - g(p1) + g(displacement) ))
                # print(g(location), g(p1))
                if abs( g(location) - g(p1) + g(displacement) ) <= radius: # + g(size)/2:
                    return True
            return False

        checkCollision = lambda p1,p2,direction : calc(p1,p2, self.RADIUS, location, displacement, size, direction)
        
        def check(p1,p2,d):
            if checkCollision(p1,p2,d): self.reflect(d)
        
        h = Direction.Horizontal
        v = Direction.Vertical

        collision = check(p[2], p[1], h)  or check(p[3], p[0], h) or check(p[1], p[0], v) or check(p[2],p[3],v)
        
        checkEdge = lambda p, center, radius: (p-center).size() < radius
        checkCollisionOnEdge = lambda p: checkEdge(p, Vector(self.location), self.RADIUS)
        
        collision2 = sum( list( map( checkCollisionOnEdge, p[:-1] ) ) ) > 0
        
        if collision2: 
            pass
            
        return collision or collision2

    def reflect(self, c):
        d = self.direction 
        if c == Direction.Horizontal:
            self.changeDirection(Vector( d.x , -d.y ))
        else:
            self.changeDirection(Vector( -d.x, d.y ))
        # print("reflecting on",c)

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

    # def checkHorizontalCollision(self, ball):
        

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

