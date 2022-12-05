import pyxel
from random import randint, random

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

WINDOW_WIDTH = 160
WINDOW_HEIGHT = 120

STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 14

BALL_WIDTH = 8
BALL_HEIGHT = 8
BALL_VX = 1
BALL_VY = 1
BALL_SPEED = 1

BAR_X = 0
BAR_Y = int(WINDOW_HEIGHT*2/3)
BAR_WIDTH = 32
BAR_HEIGHT = 4
BAR_SPEED = 5

SCORE = 0
HIGEEST_SCORE = 0
LIFE = 5

class Background:
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append((
                random() * pyxel.width, 
                random() * pyxel.height, 
                random() * 1.5 + 1
            ))

    def update(self):
        for i, (x, y, speed) in enumerate(self.star_list):
            y -= speed
            if y <= 0:
                y += pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.star_list:
            if speed > 1.8:
                pyxel.pset(x, y, STAR_COLOR_HIGH)
                
            else :
                pyxel.pset(x, y, STAR_COLOR_LOW) 
                
class Ball:
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.vx = BALL_VX
        self.vy = BALL_VY
        self.speed = BALL_SPEED

        self.score = SCORE
        self.life = LIFE

    def update(self,time):
        self.speed = (pyxel.frame_count - time)//200+1

        if self.x <= 0:
            self.vx = self.speed
        
        if self.x >= pyxel.width - BALL_WIDTH:
            self.vx = -self.speed

        if self.y <= 0:
            self.vy = self.speed

        if self.y >= pyxel.height - BALL_HEIGHT:
            self.vy = -self.speed
            self.life -= 1

        self.x += self.vx
        self.y += self.vy
        
    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            0,
            32,
            0,
            BALL_WIDTH,
            BALL_HEIGHT,
            12,
        )


class Bar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = BAR_SPEED   

    def update(self):
        if (pyxel.btnp(pyxel.KEY_A, 1, 1)
            or pyxel.btnp(pyxel.KEY_LEFT, 1, 1)):
            self.x -= self.speed

        if (pyxel.btnp(pyxel.KEY_D, 1, 1)
            or pyxel.btnp(pyxel.KEY_RIGHT, 1, 1)):
            self.x += self.speed
        
        if self.x <= 0:
            self.x = 0

        if self.x >= pyxel.width - BAR_WIDTH:
            self.x = pyxel.width - BAR_WIDTH

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            0,
            0,
            0,
            BAR_WIDTH,
            BAR_HEIGHT,
            12,
        )


class App:
    def __init__(self):
        #pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="pingpong", quit_key=pyxel.KEY_Q)
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="pingpong", quit_key=pyxel.KEY_Q)

        pyxel.load("my_resource.pyxres")

        self.scene = SCENE_TITLE

        self.highest_score = HIGEEST_SCORE

        self.background = Background()
        self.ball = Ball(
            randint(20,WINDOW_WIDTH-20), 
            randint(20,WINDOW_HEIGHT-20)
            )
        self.bar = Bar(BAR_X, BAR_Y)

        pyxel.run(self.update, self.draw)

    def update(self):

        self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start_time = pyxel.frame_count
            self.scene = SCENE_PLAY
            
    def update_play_scene(self):

        self.ball.update(self.start_time)
        self.bar.update()

        if self.ball.vy > 0:

            if (
                self.bar.y <= self.ball.y + BALL_HEIGHT
                and self.ball.y + BALL_HEIGHT <= self.bar.y + BAR_HEIGHT

                and self.ball.x + BALL_WIDTH/2 >= self.bar.x 
                and self.ball.x + BALL_WIDTH/2 <= self.bar.x + BAR_WIDTH
            ):

                self.ball.vy = -self.ball.speed
                self.ball.score += 10 * self.ball.speed
            
        elif self.ball.vy < 0:

            if (
                self.bar.y <= self.ball.y
                and self.ball.y <= self.bar.y + BAR_HEIGHT

                and self.ball.x + BALL_WIDTH/2 >= self.bar.x 
                and self.ball.x + BALL_WIDTH/2 <= self.bar.x + BAR_WIDTH
            ):

                self.ball.vy = self.ball.speed
                self.ball.score += 10 * self.ball.speed
                    
        else:
            pass
                         
        if self.ball.life <= 0:
            self.scene = SCENE_GAMEOVER
           
    def update_gameover_scene(self):

        if self.highest_score < self.ball.score:
            self.highest_score = self.ball.score

        if pyxel.btnp(pyxel.KEY_RETURN):
            #スコア等のリセット
            self.ball = Ball(randint(20,140), randint(20,100))

            self.ball.vy = BALL_VY
            self.ball.speed = BALL_SPEED

            self.bar.x = BAR_X
            self.bar.y = BAR_Y

            self.ball.score = SCORE
            self.ball.life = LIFE

            self.scene = SCENE_TITLE


    def draw(self):
        pyxel.cls(10)

        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

    def draw_title_scene(self):
        self.x = int(pyxel.width/2) - 30
        self.y = int(pyxel.height*2/3)
 
        pyxel.text(self.x, self.y,    " Pyxel Pingpong", pyxel.frame_count % 16)
        pyxel.text(self.x, self.y+14, "- PRESS ENTER -", 0)

    def draw_play_scene(self):
        #pyxel.blt(x, y, img, u, v, w, h, [colkey])

        self.ball.draw()
        self.bar.draw()

        for i in range(self.ball.life):
            pyxel.blt(
                pyxel.width-10*(i+1),
                4,
                0,
                40,
                0,
                8,
                8,
                12,
            )

        s = "SCORE {:>4}".format(self.ball.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)

        v = "SPEED {:>4}".format(self.ball.speed)
        pyxel.text(5, 10, v, 1)
        pyxel.text(4, 10, v, 7)

        h = "HIGH  {:>4}".format(self.highest_score)
        pyxel.text(5, 16, h, 1)
        pyxel.text(4, 16, h, 7)        


    def draw_gameover_scene(self):

        s = "SCORE {:>4}".format(self.ball.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)

        v = "SPEED {:>4}".format(self.ball.speed)
        pyxel.text(5, 10, v, 1)
        pyxel.text(4, 10, v, 7)

        h = "HIGH  {:>4}".format(self.highest_score)
        pyxel.text(5, 16, h, 1)
        pyxel.text(4, 16, h, 7)        

        pyxel.text(self.x, self.y-14, "   GAME OVER   ", pyxel.frame_count % 16)
        pyxel.text(self.x, self.y,    "- PRESS ENTER -", 0)
        pyxel.text(self.x, self.y+14, "- QUIT    Q   -", 0)

App()