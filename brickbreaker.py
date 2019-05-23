print("((BREAK BREAKER))\nMade by: Me")

import turtle
import time
from datetime import datetime, timedelta
import threading

#import my own classes
from vector import Vector
# import game_objects
from game_objects import Arrow, Brick, Wall, Ball
from gamemanager import GameManager

class Game:
    balls = []
    bricks = []

    def __init__(self):
        super().__init__()

        self.ui = UI()
        self.InitializeUI()
        self.setKeyEvents()

        updateThread = threading.Timer(0.3, self.Update)
        updateThread.name = "Update Thread"
        updateThread.start()
        
    def InitializeUI(self):
        self.arrow = Arrow()
        # self.bricks.append( Brick() )
        # self.balls.append( Ball() )


    def setKeyEvents(self):
        win = self.ui.window
        win.onkeypress(self.arrow.tiltLeft, "Left")
        win.onkeypress(self.arrow.tiltRight, "Right")
        win.onkeyrelease(self.arrow.stopTilting, "Left")
        win.onkeyrelease(self.arrow.stopTilting, "Right")
        win.onkeypress(self.shoot, "space")
        win.onkeypress(self.Quit, "q")

    def shoot(self):
        arrow = self.arrow
        direction = Vector.i(arrow.angle)
        initPos = arrow.turtle.pos() + direction.toVec2D()*(Ball.RADIUS*2 + arrow.length)
        n = 4
        
        d = Ball.RADIUS*2.1
        for i in range(n):
            ball = Ball(initPos, direction, d / Ball.speed * i)
            self.balls.append(ball)
            # balls[i].object.forward(d*i)


            # time.sleep(0.1)
            # time.sleep(1/UI.FRAMERATE)

    def tick(self):
        now = datetime.now()
        try: self.deltaTime = (now - self.lastCall).total_seconds()
        except: self.deltaTime = 1/self.ui.FRAMERATE
        self.lastCall = now
   
    def Refresh(self, object ):
        object.refresh(self.deltaTime)
        return type(object)

    def Update(self):

        while True:
            self.tick()
            # gameObjects = [ self.arrow ] + self.balls
            # self.arrow.refresh(self.deltaTime)
            # for obj in self.balls:
                # obj.refresh(self.deltaTime)
            # print(self.deltaTime, 1/GameManager.FRAMERATE)
            
            self.Refresh(self.arrow)
            list( map(self.Refresh, self.balls) )
            # print(list(x))
            # time.sleep(0.005)
            self.ui.window.update()

    def Quit(self):
        print("BYE!")
        self.ui.window.bye()
        quit(0)

class UI:
    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600
    # FRAMERATE = 30
    # deltaTime = 1/FRAMERATE
    FRAMERATE = GameManager.FRAMERATE
    
    def __init__(self):
        super().__init__()
        from turtle import Screen, Turtle
        win = Screen()
        win.tracer(0,0) 
        win.bgcolor("dark grey")
        # win.setup(0,0)
        win.title("Another Brick Breaker Game :))")
        win.setup(self.SCREEN_WIDTH*1.5, self.SCREEN_HEIGHT*2) 
        # win.screensize(canvwidth=self.SCREEN_WIDTH, canvheight=self.SCREEN_HEIGHT)
        win.listen()
        self.window = win
        
        self.pen = Turtle()
        # self.pen.hideturtle()
        self.pen.pensize(3)
        self.pen.up()
        self.pen.goto(-self.SCREEN_WIDTH*0.4, self.SCREEN_HEIGHT/2 )
        self.importTextures()
        self.drawScreenUI()

    def importTextures(self):
        soccerball = "ball.gif"
        win = self.window
        win.addshape("ball.gif")

    def drawScreenUI(self):
        self.pen.write("Yet Another Brickbreaker Game!",font= ('Arial', 20) )

    def refresh(self):
        pass

game = Game()
print("Started Game ^^")
game.ui.window.mainloop()
