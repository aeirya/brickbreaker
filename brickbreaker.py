print("((BREAK BREAKER))\nMade by: Me")

import turtle
import time
from datetime import datetime, timedelta
import threading

#import my own classes
from vector import Vector
from game_objects import Arrow, Brick, Wall, Ball

class Game:

    gameObjects = []
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
        initPos = Vector(tuple(arrow.turtle.pos())) + direction*(Ball.RADIUS*3 + arrow.length)
        for i in range(2):
            self.balls.append( Ball( initPos, direction ) ) 
            time.sleep(1/UI.FRAMERATE)

    def Update(self):
        gameObjects = [ self.arrow, self.ui ] + self.balls + self.bricks
        
        while True:
            
            for obj in gameObjects:
                obj.refresh()
            time.sleep(0.005)
            self.ui.window.update()

    def Quit(self):
        print("BYE!")
        self.ui.window.bye()
        quit(0)

class UI:
    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600
    FRAMERATE = 30
    deltaTime = 1/FRAMERATE
    
    def __init__(self):
        super().__init__()

        from turtle import Screen
        win = Screen()
        win.tracer(0,0) 
        win.bgcolor("dark grey")
        win.setup(0,0)
        win.title("Another Brick Breaker Game :))")
        win.setup(self.SCREEN_WIDTH*1.5, self.SCREEN_HEIGHT*2) 
        win.screensize(canvwidth=self.SCREEN_WIDTH, canvheight=self.SCREEN_HEIGHT)
        win.listen()
        self.window = win

    def refresh(self):
        pass

game = Game()
print("Started Game ^^")
game.ui.window.mainloop()
