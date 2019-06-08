print("((BREAK BREAKER))\nMade by: Me")

import turtle
import time
from datetime import datetime, timedelta
import threading

#import my own classes
from vector import Vector
from game_objects import Arrow, Brick, Wall, Ball, Direction
from gamemanager import GameManager, Shape, Mode
import gamemanager

class Game:
    balls = []
    bricks = []
    number_of_balls = 1
    level = 2
    gamemode = Mode.Classic
    paused = False

    def __init__(self):
        super().__init__()

        self.ui = UI()
        self.InitializeUI()
        self.setKeyEvents()
        
        self.startGame()

    def startGame(self, mode= Mode.Classic):
        self.paused = False
        self.gamemode = mode

        updateThread = threading.Timer(0.3, self.Update)
        updateThread.name = "Update Thread"
        updateThread.start()

    addBrick = lambda self, n: self.bricks.append( Brick( self.ui.squares[0][n] ) )
    
    def generateBricks(self):
        from random import sample
        from math import sqrt, floor
        f = lambda x : floor( sqrt(2 * x) ) #formula to be changed
        n = f( self.level )
        bricks = sample( list(range(6)) , n )
        list( map( self.addBrick, bricks ) )
    
    def clearScene(self):
        def clearList(objects):
            for i, obj in enumerate(objects):
                objects[i].destroy()
                del objects[i]
        # delList = [ self.walls, self.balls, self.bricks, [self.arrow] ]
        # self.paused = True
        delList = [ self.bricks ]
        # list( map( clearList, delList ) )
        for queue in delList:
            clearList(queue)
        self.ui.window.update()

    def InitializeUI(self):
        self.arrow = Arrow()
        # self.generateBricks()
        self.setupWalls()

        self._testScenario()
        
        # print(self.arrow.pivotPoint)
        
    def setupWalls(self):
        points = [ (1,0), (-1,0) , (0,1), (0,-1) ]
        w,h = UI.SCREEN_WIDTH/2 * Wall.a , UI.SCREEN_HEIGHT/2 * Wall.b

        points = list( map( lambda x: (x[0]*w, x[1]*h), points ) )
        self.walls = [ Wall(p, Direction.Horizontal if p[0]==0.0 else Direction.Vertical) for p in points ]

    def addBrick(self, X, initialHealth = 1 ):
        self.bricks.append( Brick( self.ui.squares[X[0]][X[1]] , initialHealth ) )

    def _testScenario(self):
        for i in range(1,5,3):
            for x in self.ui.squares[i]:
                self.bricks.append( Brick(x) )      
        
        for i in range(3,6, 2):
            self.bricks.append( Brick( self.ui.squares[i][-1] , 3 ) )
            self.bricks.append( Brick( self.ui.squares[i][0]))

        self.addBrick( (7,5) , 2 )
        # self.bricks.append( Brick( self.ui.squares[3][-2]))

    def setKeyEvents(self):
        win = self.ui.window
        win.onkeypress(self.arrow.tiltLeft, "Left")
        win.onkeypress(self.arrow.tiltRight, "Right")
        win.onkeyrelease(self.arrow.stopTilting, "Left")
        win.onkeyrelease(self.arrow.stopTilting, "Right")
        win.onkeypress(self.shoot, "space")
        win.onkeypress(self.Quit, "q")
        win.onkeypress(self.arrow.drawLine, 'v')
        # win.onkeypress( lambda: self.gamemode = Mode.Classic if self.gamemode == Mode.Classic else Mode.Chaos , 's') #Needs to be refined
        win.onkeypress(self.clearScene, 'w')
        # win.onkeyrelease(self.arrow.clearDotter, 'v')
        ''']
        t = turtle.Turtle()
        def hello(x,y):
            print( x,y )
        t.shape("circle")
        t.shapesize(10,10)
        t.ondrag( hello )
        # print(x)
        '''
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
        #Framerate control
        accumulator = 0
        while True:
            self.tick()
            accumulator += self.deltaTime
            if accumulator < 1/UI.FRAMERATE:
                time.sleep(self.deltaTime) #A little delay may be good
                continue
            else: 
                self.deltaTime = accumulator
                # print(accumulator)
                accumulator = 0
            #Start Updating objects
            self.Refresh(self.arrow)
            list( map(self.Refresh, self.balls) )
            # list( map(Brick.refresh, self.bricks) )
            # list( map(Ball.checkCollision, self.balls, self.bricks) )

            for ballID, ball in enumerate( self.balls ):
                l = list( map(ball.collides, self.walls) )
                
                if l[3] == True: #Hit the floor
                    if self.gamemode == Mode.Classic:
                        ball.destroy()
                        del self.balls[ballID]
                    if self.gamemode == Mode.Chaos: pass
                
                if True in l: continue #No need to check bricks

                for i, brick in enumerate( self.bricks ) :
                    event = ball.collides(brick)
                    if event: 
                        brick.loseHealth()
                        if brick.health <= 0:
                            del self.bricks[i]
                        break
            self.ui.window.update()
            if self.paused: break
            # t = turtle.Turtle()
            # print( t.screen.cv.winfo_pointerx() - self.arrow.MouseZeroX )
        
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

def help():
    print("You can play using left and right arrows\n"+
        "Press Space to shoot\n"+
        "Press V for aim assitance\n"+
        "Press Q to exit the game (don't! :( )"
        )
game = Game()
print("Started Game ^^")
help()
game.ui.window.mainloop()
