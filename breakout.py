import pygame
from math import *
import tkinter
import random
import time
root = tkinter.Tk()
resolution = [root.winfo_screenwidth(), root.winfo_screenheight()]
screen = pygame.display.set_mode(resolution)

global extraBalls


def collisions(blocks, p, circ, res):
    bCenter = circ.getPos()
    bRadius = circ.getRad()
    bVel = circ.getVel()
    px, py, pw, ph = p.getRect()
    if py < (bCenter[1]+bRadius) < py+ph+bRadius*2 and px-bRadius < (bCenter[0]) < px+pw+bRadius:
        depth = py - (bCenter[1]+bRadius)
        circ.changePos([bCenter[0], bCenter[1]+depth])
        bVel[1] = bVel[1]*-1
        bVel[0] = (bCenter[0] - (px+0.5*pw))*0.02

    if bCenter[0] < 0 or bCenter[0] > res[0]:
        bVel[0] = bVel[0]*-1
    if bCenter[1] < 0:
        bVel[1] = bVel[1]*-1
    if bCenter[1] > res[1]:
        return True

    for b in blocks:
        bx, by, bw, bh = b.getRect()
        tick = circ.getTick()
        if tick != circ.limit:
            ignore = True
        else:
            ignore = False
        collision = False
        top = [[bx, by-10], [bx+bw, by+10]]
        bottom = [[bx, by+bh-10], [bx+bw, by+bh+10]]
        left = [[bx-10, by], [bx+10, by+bh]]
        right = [[bx+bw-10, by], [bx+bw+10, by+bh]]
        if top[0][0] < bCenter[0] < top[1][0] and top[0][1] < bCenter[1]+bRadius < top[1][1]:
            if not ignore:
                bVel[1] = bVel[1]*-1
                circ.setTick(0)
            else:
                circ.setTick(tick+1)
            collision = True
        if bottom[0][0] < bCenter[0] < bottom[1][0] and bottom[0][1] < bCenter[1]-bRadius < bottom[1][1]:
            if not ignore:
                bVel[1] = bVel[1]*-1
                circ.setTick(0)
            else:
                circ.setTick(tick+1)
            collision = True
        if left[0][0] < bCenter[0]+bRadius < left[1][0] and left[0][1] < bCenter[1] < left[1][1]:
            if not ignore:
                bVel[0] = bVel[0]*-1
                circ.setTick(0)
            else:
                circ.setTick(tick+1)
            collision = True
        if right[0][0] < bCenter[0]-bRadius < right[1][0] and right[0][1] < bCenter[1] < right[1][1]:
            if not ignore:
                bVel[0] = bVel[0]*-1
                circ.setTick(0)
            else:
                circ.setTick(tick+1)
            collision = True
        if collision:
            perk = b.getPerk()
            if perk == "Pierce":
                circ.increaseLimit()
            if perk == "Scatter":
                for k in range(2):
                    x = random.randint(1, 2)
                    y = random.randint(1, 2)
                    velocity = [x, y]
                    Clone = Ball(bCenter[0], bCenter[1], 7, (255, 0, 255))
                    Clone.changeVelocity(velocity)
                    extraBalls.append(Clone)
                    velocity = [-x, -y]
                    Clone = Ball(bCenter[0], bCenter[1], 7, (255, 0, 255))
                    Clone.changeVelocity(velocity)
                    extraBalls.append(Clone)
            if perk == "Upgrade":
                p.upgrade()

            blocks.remove(b)
    circ.changeVelocity(bVel)


class Block:
    def __init__(self, x, y, w, h, colour):
        perkChance = random.randint(1, 5)
        self.perk = None
        perk = 0
        chance = 0
        if perkChance == 5:
            perk = random.randint(1, 3)
            if perk == 1:
                chance = random.randint(1, 3)
                if chance == 1:
                    self.perk = "Scatter"
                if chance == 3:
                    self.perk = "Upgrade"
                    perk = 3
            if perk == 2 or perk == 4:
                self.perk = "Pierce"
            if perk == 3 or perk == 5:
                self.perk = "Upgrade"
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour
        if perkChance == 5:
            if perk == 1:
                if chance == 1:
                    self.colour = [0, 0, 253]
            elif perk == 2:
                self.colour = [0, 253, 0]
            elif perk == 3:
                self.colour = [253, 0, 0]

    def getRect(self):
        return self.x, self.y, self.w, self.h

    def getPerk(self):
        return self.perk

    def draw(self):
        if self.perk == "Scatter":
            self.colour[2] += 1
            if self.colour[2] + 1 > 256:
                self.colour[2] = 120
        elif self.perk == "Pierce":
            self.colour[1] += 1
            if self.colour[1] + 1 > 256:
                self.colour[1] = 120
        elif self.perk == "Upgrade":
            self.colour[0] += 1
            if self.colour[0] + 1 > 256:
                self.colour[0] = 120

        pygame.draw.rect(screen, self.colour, [self.x, self.y, self.w, self.h])


class Paddle:
    def __init__(self, x, y, w, h, colour):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour

    def getRect(self):
        return self.x, self.y, self.w, self.h

    def upgrade(self):
        factor = 50
        self.x -= 0.5*factor
        self.w += factor

    def draw(self):
        pygame.draw.rect(screen, self.colour, [self.x, self.y, self.w, self.h])

    def move(self, x):
        self.x += x


class Ball:
    def __init__(self, x, y, r, colour):
        self.perk = None
        self.tick = 0
        self.limit = 0
        self.center = [x, y]
        self.radius = r
        self.colour = colour
        self.velocity = [0, 0]

    def getPos(self):
        return self.center

    def getRad(self):
        return self.radius

    def getVel(self):
        return self.velocity

    def changePos(self, newPos):
        self.center[0] = newPos[0]
        self.center[1] = newPos[1]

    def draw(self):
        pygame.draw.circle(screen, self.colour, self.center, self.radius)

    def move(self):
        self.center[0] += self.velocity[0]
        self.center[1] += self.velocity[1]

    def changeVelocity(self, vector):
        self.velocity[0] = vector[0]
        self.velocity[1] = vector[1]

    def addPerk(self, perk):
        self.perk = perk

    def getPerk(self):
        return self.perk

    def getTick(self):
        return self.tick

    def setTick(self, tick):
        self.tick = tick

    def getLimit(self):
        return self.limit

    def increaseLimit(self):
        self.limit += 1


blockList = []
bWidth = 103
gap = 5
bHeight = 30
numberAcross = round(((resolution[0]-gap) / (bWidth+gap))//1)
numberDown = 6
for j in range(numberDown):
    for i in range(numberAcross):
        x1 = i*(bWidth+gap)+gap
        y1 = (j*(bHeight+gap)+gap)+100
        c = (100, 100, 100)
        NewBlock = Block(x1, y1, bWidth, bHeight, c)
        blockList.append(NewBlock)
        NewBlock.draw()
        pygame.display.flip()
        time.sleep(0.005)

running = True
paused = False
paddle = Paddle(resolution[0]/2-40, resolution[1]-100, 80, 20, (255, 255, 255))
ball = Ball(resolution[0]/2-5, resolution[1]-400, 10, (255, 0, 0))
ball.changeVelocity([0, 2])

extraBalls = []
speed = 1.5

while running:
    if not paused:
        screen.fill((0, 0, 0))
        failState = collisions(blockList, paddle, ball, resolution)
        ball.move()
        if len(extraBalls) != 0:
            for b in extraBalls:
                death = collisions(blockList, paddle, b, resolution)
                b.move()
                b.draw()
                if death:
                    extraBalls.remove(b)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_d]:
            paddle.move(speed)
        if keys[pygame.K_d] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            paddle.move(1.75*speed)
        if keys[pygame.K_a]:
            paddle.move(-speed)
        if keys[pygame.K_a] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            paddle.move(-1.75*speed)

        pos = ball.getPos()
        vel = ball.getVel()
        magnitude = sqrt(vel[0]**2 + vel[1]**2)
        for i in range(1, 10):
            center = [pos[0]-vel[0]*10, pos[1]-vel[1]*10]
            center[0] -= vel[0]*i*2*magnitude**2
            center[1] -= vel[1]*i*2*magnitude**2
            radius = 5 - i//2
            pygame.draw.circle(screen, (100, 0, 0), center, radius)
        ball.draw()
        for block in blockList:
            block.draw()
        paddle.draw()

        pygame.display.flip()
        if failState:
            time.sleep(1)
            running = False

        if len(blockList) == 0:
            print("YOU WIN")
            time.sleep(1)
            running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

pygame.quit()
