print("((BREAK BREAKER))\nMade by: Me")

import turtle
import time
from datetime import datetime, timedelta
import threading

#import my own classes
from vector import Vector
from game_objects import Arrow, Brick, Wall, Ball
from gamemanager import GameManager, Shape
import gamemanager

class Game:
    balls = []
    bricks = []
    number_of_balls = 1
    
    def __init__(self):
        super().__init__()

        self.ui = UI()
        self.InitializeUI()
        self.setKeyEvents()

        updateThread = threading.Timer(0.3, self.Update)
        updateThread.name = "Update Thread"
        updateThread.start()

    def InitializeUI(self):
        # y = self.ui.SCREEN_HEIGHT
        # x = self.ui.SCREEN_WIDTH 
        self.arrow = Arrow()

        for i in range(1):
            for x in self.ui.squares[i]:
                self.bricks.append( Brick(x) )      
        
        for i in range(3,6):
            self.bricks.append( Brick( self.ui.squares[i][-1]  ) )
            self.bricks.append( Brick( self.ui.squares[i][0]))

        self.bricks.append( Brick( self.ui.squares[3][-2]))

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
        initPos = arrow.turtle.pos() + direction.toVec2D() * (arrow.length * 2 + Ball.RADIUS)
        d = Ball.RADIUS*2.1
        for i in range(self.number_of_balls):
            ball = Ball(initPos, direction, d / Ball.speed * (i+1) )
            self.balls.append(ball)

    def tick(self):
        now = datetime.now()
        try: self.deltaTime = (now - self.lastCall).total_seconds()
        except: self.deltaTime = 1/self.ui.FRAMERATE/10
        self.lastCall = now
   
    def Refresh(self, object ):
        object.refresh(self.deltaTime)

    def Update(self):

        while True:
            self.tick()
            self.Refresh(self.arrow)
            list( map(self.Refresh, self.balls) )
            list( map(Brick.refresh, self.bricks) )
            # list( map(Ball.checkCollision, self.balls, self.bricks) )

            for ball in self.balls:
                # for brick in self.bricks:
                for i,brick in enumerate(self.bricks):
                    # print(i)
                    event = ball.collides(brick)
                    if event: break

            # time.sleep(0.001)

            self.ui.window.update()

    def Quit(self):
        print("BYE!")
        self.ui.window.bye()
        quit(0)

class UI:
    SCREEN_WIDTH, SCREEN_HEIGHT = gamemanager.UI.SCREEN_WIDTH, gamemanager.UI.SCREEN_HEIGHT
    FRAMERATE = GameManager.FRAMERATE
    # SQUARES = (8,4)
    def __init__(self):
        super().__init__()
        from turtle import Screen, Turtle
        win = Screen()
        win.tracer(0,0) 
        win.bgcolor("dark grey")
        # win.bgcolor("#029ed2")
        win.title("Another Brick Breaker Game :))")
        win.setup(self.SCREEN_WIDTH*1.5, self.SCREEN_HEIGHT*1.5) 
        win.screensize(canvwidth=self.SCREEN_WIDTH, canvheight=self.SCREEN_HEIGHT)
        win.listen()
        self.window = win
        
        self.pen = Turtle()
        self.pen.hideturtle()
        self.pen.pensize(3)
        self.pen.up()
        self.pen.goto( -180, self.SCREEN_HEIGHT/4 )
        self.importTextures()
        self.drawScreenUI()
        self.generateSquares()

    # from turtle import Vec2D
    def generateSquares(self):
        self.squares = []
        sq = self.squares
        for i in range(9):
            line = []
            for j in range(6):
                p = turtle.Vec2D( (UI.SCREEN_WIDTH+5)*(j-3)/6 + Brick.size[0]/2  , ( UI.SCREEN_HEIGHT + 25) *(4.5-i)/9 )
                line.append(p)
            sq.append(line)

    def importTextures(self):
        soccerball = Shape.soccerball
        win = self.window
        win.addshape(soccerball)

        # Not going to be used for now
        # brick = Shape.brick
        # win.addshape(brick)
        
    def drawScreenUI(self):
        self.pen.write("Yet Another Brickbreaker Game!",font= ('Arial', 20) )

    def refresh(self):
        pass

game = Game()
print("Started Game ^^")
game.ui.window.mainloop()

