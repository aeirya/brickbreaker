class GameManager:
    #Game Object Consts.
    BALL_VELOCITY = 12.5
    ARROW_VELOCITY = 2.2
    # BALL_RADIUS = 10
    BALL_RADIUS = 17
    #Video Setttings
    FRAMERATE = 60
    # Screen_Size = (X,Y)

class UI:
    # SCREEN_WIDTH, SCREEN_HEIGHT = 600, 450
    x = 80
    SCREEN_WIDTH, SCREEN_HEIGHT = 12 * x, 9 * x
class Shape:
    soccerball = "Textures/ball.gif"
    # brick = "brick.gif"

class Mode:
    Classic = 0
    Chaos = 1