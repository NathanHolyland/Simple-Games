import pygame
import math
import time
from math import *
resolution = [1600, 900]
screen = pygame.display.set_mode(resolution)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def unit(self):
        if self.magnitude() == 0:
            return Vector(0, 0)
        return Vector(self.x/self.magnitude(), self.y/self.magnitude())

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def sub(self, v):
        return Vector(self.x - v.x, self.y - v.y)

    def multiply(self, n):
        return Vector(self.x*n, self.y*n)

    def vec(self):
        return [self.x, self.y]


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def multiply(self, vector):
        newVec = []
        for r in self.matrix:
            row = 0
            for c in range(len(r)):
                row += r[c] * vector[c]
            newVec.append(row)

        return [newVec[0], newVec[1]]

    def get(self):
        return self.matrix


class Ball:
    def __init__(self, x, y, velocity):
        self.radius = 5
        self.colour = (255, 0, 0)
        self.position = Vector(x, y)
        self.velocity = velocity

    def move(self):
        self.position = self.position.add(self.velocity)

    def draw(self):
        pygame.draw.circle(screen, self.colour, self.position.vec(), self.radius, 0)

    def addVelocity(self, v):
        self.velocity = self.velocity.add(v)

    def getCenter(self):
        return self.position.vec()


class Cannon:
    def __init__(self, points):
        self.points = points
        self.rotation = 0

    def draw(self):
        pygame.draw.lines(screen, (255, 0, 0), True, self.points, 3)

    def rotate(self, rotation, center):
        rotation = rotation * pi/180
        self.rotation = self.rotation + rotation
        points = []
        rotationMatrix = Matrix([[cos(rotation), sin(rotation)],
                                 [-sin(rotation), cos(rotation)]])
        for point in self.points:
            newPoint = [point[0] - center[0], point[1] - center[1]]
            newPoint = (rotationMatrix.multiply(newPoint))
            newPoint = [newPoint[0] + center[0], newPoint[1] + center[1]]
            points.append(newPoint)
        self.points = points

    def updateAxle(self, a):
        r = self.rotation
        self.points = [a, [a[0] + 50, a[1]], [a[0] + 50, a[1] - 25], [a[0], a[1] - 25]]
        rotationMatrix = Matrix([[cos(r), sin(r)],
                                 [-sin(r), cos(r)]])
        points = []
        for point in self.points:
            newPoint = [point[0] - a[0], point[1] - a[1]]
            newPoint = (rotationMatrix.multiply(newPoint))
            newPoint = [newPoint[0] + a[0], newPoint[1] + a[1]]
            points.append(newPoint)
        self.points = points

    def fire(self, power):
        p1 = Vector(self.points[1][0], self.points[1][1])
        p2 = Vector(self.points[2][0], self.points[2][1])
        vector = p2.sub(p1)
        vector = vector.multiply(0.5)
        center = p1.add(vector)
        center = center.vec()

        dx = self.points[1][0] - self.points[2][0]
        dy = self.points[1][1] - self.points[2][1]
        gradient = dy/dx
        firedGrad = -1/gradient
        signY = dy/abs(dy)
        launchVec = Vector(signY, firedGrad*signY)
        launchVec = launchVec.unit()
        print(launchVec.vec())
        launchVec = launchVec.multiply(power)

        newBall = Ball(center[0], center[1], launchVec)
        return newBall


class Planet:
    def __init__(self, radius, colour):
        self.radius = radius
        self.mass = radius**2/10000
        self.colour = colour
        self.center = [(resolution[0]/2), resolution[1] + self.radius-200]

    def draw(self):
        pygame.draw.circle(screen, self.colour, self.center, self.radius, 0)

    def getY(self, x):
        a = self.center[0]
        b = self.center[1]
        r = self.radius
        y1 = sqrt(r**2-x**2+2*a*x-a**2)+b
        y2 = -1*sqrt(r**2-x**2+2*a*x-a**2)+b
        return min(y1, y2)

    def changeRadius(self, x):
        self.center[1] = self.center[1] + x
        self.radius += x
        self.mass = self.radius**2/10000

    def getRadius(self):
        return self.radius


def orbit(obj, planet):
    center = obj.getCenter()
    gravity = Vector(planet.center[0] - center[0], planet.center[1] - center[1])
    factor = gravity.magnitude()
    gravity = gravity.unit()
    gravity = gravity.multiply(200/(factor**2))
    gravity = gravity.multiply(planet.mass)
    gravity.vec()
    obj.addVelocity(gravity)


def collision(obj, planet):
    center = obj.position
    pCenter = Vector(planet.center[0], planet.center[1])
    distance = center.sub(pCenter)
    distance = distance.magnitude()
    if distance < obj.radius + planet.radius:
        correction = distance - (obj.radius + planet.radius)
        direction = obj.velocity.unit()
        correction = direction.multiply(correction)
        ball.position = ball.position.add(correction)
        obj.velocity = Vector(0, 0)


running = True

earth = Planet(1000, (0, 200, 100))
axle = [300, earth.getY(300)]

can = Cannon([axle, [axle[0]+50, axle[1]], [axle[0]+50, axle[1]-25], [axle[0], axle[1]-25]])
can.rotate(45, axle)
balls = []
power = 2
while running:
    screen.fill((255, 255, 255))
    earth.draw()
    can.draw()
    for ball in balls:
        orbit(ball, earth)
        collision(ball, earth)
        ball.move()
        ball.draw()
    pygame.draw.rect(screen, (255, 0, 0), [20, 551, 20, 248], 0)
    pygame.draw.rect(screen, (0, 255, 0), [20, 800-power*50, 20, power*50], 0)
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        # if can.rotation < 1.555:
        can.rotate(0.3, axle)
    if keys[pygame.K_d]:
        # if can.rotation > 0:
        can.rotate(-0.3, axle)
    if keys[pygame.K_w]:
        if power + 0.005 <= 5:
            power += 0.005
    if keys[pygame.K_s]:
        if power - 0.005 >= 0:
            power -= 0.005
    if keys[pygame.K_UP]:
        if earth.getRadius() <= 10000:
            earth.changeRadius(1*earth.radius/1000)
            axle = [300, earth.getY(300)]
            can.updateAxle(axle)
    if keys[pygame.K_DOWN]:
        if earth.getRadius() >= 800:
            earth.changeRadius(-1*earth.radius/1000)
            axle = [300, earth.getY(300)]
            can.updateAxle(axle)
    if keys[pygame.K_ESCAPE]:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(balls) == 5:
                    balls.remove(balls[0])
                ball = can.fire(power)
                balls.append(ball)
                print("Points: ", can.points)
                print("Velocity: ", ball.velocity.vec())

pygame.quit()
