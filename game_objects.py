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

    def __init__(self):
        super().__init__()
        from turtle import Turtle
        self.angV = gm.ARROW_VELOCITY * gm.FRAMERATE
        self.pivotPoint = ((0, (-1)*UI.SCREEN_HEIGHT * (0.75+0.5)/2))
        self.turtle = Turtle()
        self.draw()
        self.initDotter()         
        # self.MouseZeroX, self.MouseZeroY = self.turtle.screen.cv.winfo_pointerx(), self.turtle.screen.cv.winfo_pointery()

    def initDotter(self):
        self.isDotterOn = False
        from turtle import Turtle
        dotter = Turtle()
        dotter.up()
        dotter.setpos( self.turtle.pos() )
        dotter.shape("square")
        dotter.shapesize( 0.14, 0.6 , 0.2)
 
        self.dotter = dotter
        # self.drawLine()
        self.dotter.ht()
        
    def drawLine(self):
        self.clearDotter()
        self.isDotterOn = True
        self.dotter.goto( self.turtle.pos() )
        self.dotter.setheading( self.angle )
        self.dotter.forward(25)

        from math import sin, radians
        formula = lambda angle , a, b: a + int ( b * (sin(radians(angle))) )
        f = lambda angle: formula( 2*angle, 20, 5 )
        n = f( self.angle ) if self.angle <= 90 else f( abs( 180 - self.angle ) )

        for i in range ( n ):
            self.dotter.forward(25)
            self.dotter.stamp()

    def clearDotter(self):
        self.isDotterOn = False
        self.dotter.clear()

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
        if self.tiltDirection != Direction.NONE:
            # self.dotter.clear()
            # try:
            #     self.dotter.clearstamps()
            # except:
            #     pass
            # while self.dotter.undobufferentries():
            #     self.dotter.undo()
            # self.drawLine()
            pass
 
    def tilt(self, deltaTime):
        i = self.tiltDirection
        if i == Direction.NONE: return

        if self.isDotterOn:
            self.clearDotter()

        from math import cos,sin
        deltaTeta = i* self.angV * deltaTime

        if not 0 < self.angle + deltaTeta < 180:
            return
        self.angle += deltaTeta

        ted = self.turtle
        ted.goto( (Vector.tuppleInit(self.pivotPoint) + Vector.polarInit(self.RADIUS, self.angle)).tupple() ) 
        ted.tilt( deltaTeta )

    def stopTilting(self):
        self.tiltDirection = Direction.NONE

        # self.dotter.clear()
        # self.drawLine()

    def tiltLeft(self):
        self.tiltDirection = Direction.Left

    def tiltRight(self):
        self.tiltDirection = Direction.Right

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

    def destroy(self):
        # print("I was awakened")
        self.object.clear()
        self.object.hideturtle() #issue!
        # del self.object 
    def __del__(self):
        self.destroy()

class Ball(GameObject):

    RADIUS = gm.BALL_RADIUS
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
    
    def refresh(self, deltaTime):
        if self.t > 0: 
            self.t-= deltaTime
            if self.t <= 0:
                self.object.showturtle()
        if self.t <= 0: 
            self.move(deltaTime)
            # self.Points = self.generatePoints()

    def move(self, deltaTime):
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
            
            if f(p1) <= f(location) <= f(p2):
                if abs( g(location) - g(p1) + g(displacement) ) <= radius: # + g(size)/2:
                    return True
            return False

        checkCollision = lambda p1,p2,direction : calc(p1,p2, self.RADIUS, location, displacement, size, direction)
        
        def check(p1,p2,d):
            if checkCollision(p1,p2,d): 
                self.reflect(d)
                return True
        
        h = Direction.Horizontal
        v = Direction.Vertical

        collision = check(p[2], p[1], h)  or check(p[3], p[0], h) or check(p[1], p[0], v) or check(p[2],p[3],v)
        if collision: return True

        checkEdge = lambda point, center, radius: (point-center).size() < radius
        checkCollisionOnEdge = lambda point: checkEdge(point, Vector(self.location), self.RADIUS)
        
        collision = sum( list( map( checkCollisionOnEdge, p[:-1] ) ) ) > 0
        if collision:
            # list( map( self.reflect, [Direction.Vertical, Direction.Horizontal] ) )
            x,y = self.location
            if not p[1].y <= y <= p[0].y:
                self.reflect(Direction.Horizontal)
            if not p[1].x <= x <= p[0].x:
                self.reflect(Direction.Vertical)

        '''
        collision2 = False
        for point in p[:-1]:
            if checkCollisionOnEdge(point):
                d = Direction.Horizontal
                x, y = self.location
                if x < point.getX():
                    if point in [ p[2], p[3] ]:
                        d = (Direction.Vertical)
                else:
                    if point in [ p[0], p[1] ]:
                        d = Direction.Vertical
                self.reflect(d)
                collision2 = True
                break
        if collision2 : print("yaaay")
        '''    

        return collision

    def reflect(self, c):
        d = self.direction 
        if c == Direction.Horizontal:
            self.changeDirection(Vector( d.x , -d.y ))
        else:
            self.changeDirection(Vector( -d.x, d.y ))

    # def destroy(self):
    #     self.object.clear()
    #     self.object.hideturtle()
    #     # print("bye bye!")
    # def __del__(self):
    #     self.destroy()

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
        pen.pensize(3)
        pen.begin_fill()

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

    def __init__(self, initialLocation = Vec2D(0,0), initialHealth = 1 ):  
        super().__init__(initialLocation, self.size)
        self.spawn( initialHealth )
        self.refresh()

    def refresh(self):
        hFont = ('Arial', 22)
        if self.health > 0:
            self.object.undo()
            self.object.write(self.health, font = (hFont) )
        else:
            while( self.object.undobufferentries() ):
                self.object.undo()
            self.object.clear()
            # self.object.reset()
            pass
            
    def spawn(self, intitHealth):
        self.health = intitHealth
        self.object.dot() #to cancel out the undo()

    def loseHealth(self):
        self.health -= 1
        self.refresh()

    # def __del__(self):
    #     self.destroy()
        
class Wall(Rect):
    # size = UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT
    border = UI.SCREEN_WIDTH/100
    a,b = 1.4, 1.4
    def __init__(self, initialLocation = Vec2D(0,0) , direction = Direction.Vertical ):  
        #code needs to be refined here
        # print(initialLocation[0])
        # if initialLocation[0] == 0.0: 
        #     direction == Direction.Horizontal
        if direction == Direction.Vertical:
            self.size = self.border, UI.SCREEN_HEIGHT * self.b
        else:
            self.size = UI.SCREEN_WIDTH * self.a , self.border 
        super().__init__(initialLocation, self.size)


turtleInstance = turtle.Turtle()
turtleInstance.hideturtle()
turtleInstance.up()

