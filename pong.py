import pygame
from random import randrange
import tkinter

class Paddle:
    def __init__(self, rect, color):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.color = color

    def setY(self, y):
        self.y = y

    def getRect(self):
        rect = (self.x, self.y, self.w, self.h)
        return rect

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 0)

    def move(self, dx):
        if dx < 0:
            if self.y > 0:
                self.y = self.y + dx
        if dx > 0:
            if (screen.get_height()) - self.h > self.y:
                self.y = self.y + dx


class Ball:
    def __init__(self, x, y, speed, color, radius, scoreboard):
        self.scoreboard = scoreboard
        self.defaultX = x
        self.defaultY = y
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.radius = radius
        self.xVelocity = randrange(-1, 2, 2) * speed
        self.yVelocity = 0

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setVelY(self, velocity):
        self.yVelocity = velocity

    def setVelX(self, velocity):
        self.xVelocity = velocity

    def getVelX(self):
        return self.xVelocity

    def setColor(self, color):
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)

    def move(self, paddle1, paddle2):
        reset = False
        if self.x < 0:
            self.scoreboard.addScore(1)
            reset = True
        if self.x > screen.get_width():
            self.scoreboard.addScore(0)
            reset = True
        if reset:
            self.x = self.defaultX
            self.y = self.defaultY
            self.yVelocity = 0
            self.xVelocity = randrange(-1, 2, 2) * self.speed
            self.color = (255, 255, 255)
            paddle1.setY(resolution[1]/2-(paddle1.h/2))
            paddle2.setY(resolution[1]/2-(paddle2.h/2))
        if not (0 < self.y < screen.get_height()):
            self.yVelocity = self.yVelocity * -1
        self.x = self.x + self.xVelocity
        self.y = self.y + self.yVelocity


class Scoreboard:
    def __init__(self, x, y):
        self.speedPer = "100%"
        self.score = [0, 0]
        self.x = x
        self.y = y

    def draw(self, currentSpeed, initialSpeed):
        color = (255, 255, 255)
        if self.speedPer[0]+self.speedPer[1] == "25":
            color = (255, 0, 0)
        self.speedPer = str(abs(((currentSpeed / initialSpeed) * 100)))
        txt = font.render(str(self.score[0]) + ":" + str(self.score[1]), False, (255, 255, 255))
        speed = font.render("Speed: " + self.speedPer[0]+self.speedPer[1]+self.speedPer[2]+"%", False, color)
        screen.blit(txt, (self.x, self.y))
        screen.blit(speed, (self.x-70, self.y + 30))

    def addScore(self, side):
        newScore = self.score
        if side == 0:
            newScore[0] += 1
        if side == 1:
            newScore[1] += 1
        self.score = newScore


def detectCollision(paddle1rect, paddle2rect, ball):
    pX = [paddle1rect[0], paddle1rect[0] + paddle1rect[2]]
    pY = [paddle1rect[1], paddle1rect[1] + paddle1rect[3]]
    cX = [paddle2rect[0], paddle2rect[0] + paddle2rect[2]]
    cY = [paddle2rect[1], paddle2rect[1] + paddle2rect[3]]

    if pX[0] < ball.getX() < pX[1]:
        if pY[0] < ball.getY() < pY[1]:
            newVelocityY = -1 * (((paddle1rect[1] + 0.5 * paddle1rect[3]) - ball.getY()) / 50)
            ball.setVelY(newVelocityY)
            if abs(-1.1 * ball.getVelX()) < 3.75:
                ball.setVelX(-1.025 * ball.getVelX())
            else:
                if ball.getVelX() < 0:
                    mod = 1
                else:
                    mod = -1
                ball.setVelX(3.75*mod)
                ball.setColor((255, 0, 0))
    if cX[0] < ball.getX() < cX[1]:
        if cY[0] < ball.getY() < cY[1]:
            newVelocityY = -1 * (((paddle2rect[1] + 0.5 * paddle2rect[3]) - ball.getY()) / 50)
            ball.setVelY(newVelocityY)
            if abs(-1.1*ball.getVelX()) < 3.75:
                ball.setVelX((-1.025 * ball.getVelX()))
            else:
                if ball.getVelX() < 0:
                    mod = 1
                else:
                    mod = -1
                ball.setVelX(3.75*mod)
                ball.setColor((255, 0, 0))


pygame.init()
root = tkinter.Tk()
resolution = [root.winfo_screenwidth(), root.winfo_screenheight()]
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Pong")
font = pygame.font.SysFont("Bernard MT", 40)

pRect = (resolution[0]*(60/1600), (resolution[1]/2)-resolution[1]*100/1800, resolution[0]*20/1600, resolution[1]*100/900)
cRect = (resolution[0]*(1520/1600), (resolution[1]/2)-10-resolution[1]*100/1800, resolution[0]*20/1600, resolution[1]*100/900)
player = Paddle(pRect, (255, 255, 255))
computer = Paddle(cRect, (255, 255, 255))

score = Scoreboard(770, 0)

ballSpeed = 1.5
b = Ball(800, 450, ballSpeed, (255, 255, 255), 10, score)
print(ballSpeed)

playerSpeed = 1
running = True

while running:
    screen.fill((0, 0, 0))
    player.draw()
    computer.draw()
    detectCollision(player.getRect(), computer.getRect(), b)
    b.move(player, computer)
    b.draw()
    score.draw(b.getVelX(), ballSpeed)
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_w]:
        player.move(-playerSpeed)
    if keys[pygame.K_s]:
        player.move(playerSpeed)
    if keys[pygame.K_UP]:
        computer.move(-playerSpeed)
    if keys[pygame.K_DOWN]:
        computer.move(playerSpeed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
