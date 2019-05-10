print("((BREAK BREAKER))\nMade by: Me")

import turtle

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

def rc():
    print("fuck you!")

import time
# import datetime
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

        # updateThread =threading.Thread(target=self.Update)
        updateThread = threading.Timer(0.3, self.Update)
        updateThread.name = "Update Thread"
        updateThread.start()
        # self.InitializeUI()
        
        # self.Update()
        # t1 =threading.Thread(target=self.InitializeUI)
        
        # t1.start()
        # self.Update()

    def InitializeUI(self):
        self.genBall()

    def genBall(self):
        print("generating a ball")
        self.gameObjects.append(Ball((10,10), (0,0)))

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
        # self.window = Screen()
        self.window =Screen()
        
        win = self.window
        win.bgcolor("dark grey")
        win.setup(0,0)
        # win.clear()
        win.title("Another Brick Breaker Game :))")
        # self.window.delay(0)  
        # self.window.onkey(f, "Right")
        self.arrow = Arrow()
        win.setup(UI.SCREEN_WIDTH*1.5, UI.SCREEN_HEIGHT*1.5) 
        win.screensize(canvwidth=UI.SCREEN_WIDTH, canvheight=UI.SCREEN_HEIGHT)     
        # win.delay(100000)
        # win.tracer( n=1000 )
        # window.onkey(tiltLeft, "Left")
        self.setKeyEvents()
        win.listen()

        self.pen = turtle.Turtle()
        pen = self.pen
        pen.up()
        pen.speed(0)
        pen.hideturtle()
        # win.exitonclick()
        # thread = threading.Thread(target = self.wait, args = win)
        # thread = threading.Timer(0.1, win.mainloop)
        # thread.start()
        # time.sleep(3)
        
        # win.mainloop()
        # input("Press Enter to Exit")
        # threading.Thread(target = KeyManager.start)

    # updateTimerStacks = 1
    updateTimerStacks = []

    def Update(self):
        # print("refresh")
        self.deltaTime = (datetime.now() - self.lastCallTime).total_seconds()
        # print(self.deltaTime - 1/Game.FRAMERATE)

        for gameObject in game.gameObjects:
            if gameObject != None:
                gameObject.move()
        
        timer = threading.Timer(1/Game.FRAMERATE, self.Update)
        timer.name = "Next Update"

        # upt = self.updateTimerStacks
        # if len(upt)==0:
        #     upt.append(timer)
        #     timer.start()
        # while len(upt) > 1:
        #     upt[0].cancel()
        #     del upt[0]
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
    Left, Right, NONE = 0,1,2

# turtle.speed(10)
# turtle.delay(0)
# turtle.tracer(0, 0)
#no use =/

class Arrow:

    # angV = 3 #angular velocity
    radius = 30
    angle = 0 #angle made from x axis
    tiltDirection = Direction.NONE
    # tilting = False
    tilter = None
    isTilting = False
    # tiltQueue = []
    # angV = Game.FRAMERATE/10
    angV = 3 * Game.FRAMERATE

    def __init__(self):
        super().__init__()
        # self.angV = Game.FRAMERATE/10
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
        dir = self.tiltDirection
        if dir == Direction.NONE:
            return

        from math import cos,sin, radians
        i = 1 if dir == Direction.Left else -1
        deltaTeta = i* self.angV * game.ui.deltaTime
        if 0 <= self.angle + deltaTeta <= 180:
            self.angle += deltaTeta
        else:
            deltaTeta = 0
        # if self.angle < 0:
        #     self.angle = 0
        # elif self.angle > 180:
        #     self.angle = 180

        ted = self.turtle
        teta = radians( self.angle )
        ted.goto( (Vector.tuppleInit(self.pivotPoint) + Vector(cos(teta), sin(teta))*self.radius).tupple() ) 
        ted.tilt( deltaTeta )

        if self.tilter!=None:
            self.tilter.cancel()

        self.tilter = threading.Timer(1/Game.FRAMERATE, self.tilt)
        # self.tiltQueue.append(self.tilter) 
        self.tilter.name = "Tilt Timer"
        self.tilter.start()


    def startTilting(self):     
        # if self.tilter == None:
        if not self.isTilting:
            self.isTilting = True
            self.tilt()
        

    def stopTilting(self):
        if self.isTilting:
            if self.tilter != None :
                self.tilter.cancel()
            self.isTilting = False
            self.tiltDirection = Direction.NONE
            # print("stopping tilting ;/")

    def tiltLeft(self):
        # if self.tiltDirection != Direction.Left:
        #     if self.isTilting != None:
        #         self.tilter.cancel()
        self.tiltDirection = Direction.Left
        self.startTilting()

    def tiltRight(self):
        self.tiltDirection = Direction.Right
        self.startTilting()

class GameObject:
    # location = Vector(0,0)
    # velocity = Vector(0,0)
    def __init__(self, vector= (0,0), initialLocation=(0,0), movable = False):
        self.movability = movable
        self.velocity = Vector.tuppleInit(vector) * Game.FRAMERATE
        self.location = Vector.tuppleInit(initialLocation)
        
        self.generator = game.ui.pen.clone()
        pen = self.generator
        # pen.up()
        pen.goto(initialLocation)
        

    def checkCollision(self):
        pass

    def move(self):
        self.location += self.velocity * game.ui.deltaTime
        self.checkCollision()

        pen = self.generator
        pen.clear()
        pen.goto(self.location.tupple())
        
        # print("move of gameobject class called")
    
class Ball(GameObject):
    RADIUS = 10
    def __init__(self, vector = (0,0), initialLocation = (0,0)):
        super().__init__(vector, initialLocation)
        self.draw()
        
    def draw(self, fill = False):
        pen = self.generator
        pen.down()
        if fill: pen.begin_fill()
        pen.circle(self.RADIUS)
        if fill: pen.end_fill()
        pen.up()

    def move(self):
        super().move()
        # self.location += self.velocity
        # game.ui.window.clear("red")
        # game.ui.clear()
        self.draw()
        # print("moved ball")
        
        # print(pen)

        # pen.color("dark grey")
        # pen.pensize(3)
        # self.draw()
        # pen.pensize(1)
        # pen.color("black")

        # turtle.clear()

        # turtle.Turtle().

game = Game()
print("Started Game ^^")

game.ui.window.mainloop()
# window.exitonclick()