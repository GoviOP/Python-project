import pygame
import sys
import random
from math import *
from tkinter import *

pygame.init()

width = 600
height = 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong!")
clock = pygame.time.Clock()

background = (245,245,220)
navy = (27, 38, 49)
red = (203, 67, 53)
blue = (52, 152, 219)
yellow = (244, 208, 63)

top = navy
bottom = navy
left = navy
right = navy

margin = 4

scoreLeft = 0
scoreRight = 0
maxScore = 20

font = pygame.font.SysFont("Small Fonts", 30)
largeFont = pygame.font.SysFont("Small Fonts", 60)

def boundary():
    global top, bottom, left, right
    pygame.draw.rect(display, left, (0, 0, margin, height))
    pygame.draw.rect(display, top, (0, 0, width, margin))
    pygame.draw.rect(display, right, (width-margin, 0, margin , height))
    pygame.draw.rect(display, bottom, (0, height - margin, width, margin))

    l = 25
    
    pygame.draw.rect(display, navy, (width/2-margin/2, 10, margin, l))
    pygame.draw.rect(display, navy, (width/2-margin/2, 60, margin, l))
    pygame.draw.rect(display, navy, (width/2-margin/2, 110, margin, l))
    pygame.draw.rect(display, navy, (width/2-margin/2, 160, margin, l))
    pygame.draw.rect(display, navy, (width/2-margin/2, 210, margin, l))
    pygame.draw.rect(display, navy, (width/2-margin/2, 260, margin, l))
    pygame.draw.rect(display, navy, (width/2-margin/2, 310, margin, l))
    pygame.draw.rect(display, navy, (width/2-margin/2, 360, margin, l))

class Paddle:
    def __init__(self, position):
        self.w = 10
        self.h = self.w*8
        self.paddleSpeed = 6
            
        if position == -1:
            self.x = 1.5*margin
        else:
            self.x = width - (1.5*margin + self.w)
            
        self.y = height/2 - self.h/2

    def show(self):
        pygame.draw.rect(display, navy, (self.x, self.y, self.w, self.h))

    def move(self, ydir):
        self.y += self.paddleSpeed*ydir
        if self.y < 0:
            self.y -= self.paddleSpeed*ydir
        elif self.y + self.h> height:
            self.y -= self.paddleSpeed*ydir


leftPaddle = Paddle(-1)
rightPaddle = Paddle(1)

class Ball:
    def __init__(self, color):
        self.r = 20
        self.x = width/2 - self.r/2
        self.y = height/2 -self.r/2
        self.color = color
        self.angle = random.randint(-75, 75)
        self.speed = 8

    def show(self):
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.r, self.r))

    def move(self):
        global scoreLeft, scoreRight
        self.x += self.speed*cos(radians(self.angle))
        self.y += self.speed*sin(radians(self.angle))
        if self.x + self.r > width - margin:
            scoreLeft += 1
            self.angle = 180 - self.angle
        if self.x < margin:
            scoreRight += 1
            self.angle = 180 - self.angle
        if self.y < margin:
            self.angle = - self.angle
        if self.y + self.r  >=height - margin:
            self.angle = - self.angle

    def Collision(self):
        if leftPaddle.x < self.x < leftPaddle.x + leftPaddle.w and leftPaddle.y <self.y < leftPaddle.y + leftPaddle.h:
            self.dist = leftPaddle.y+leftPaddle.h/2-self.y
            self.reldist = self.dist/(leftPaddle.h/2)
            self.angle = self.reldist*(-45)

  
        if rightPaddle.x + rightPaddle.w > self.x  + self.r > rightPaddle.x and rightPaddle.y < self.y + self.r < rightPaddle.y + rightPaddle.h:
            self.dist = rightPaddle.y+rightPaddle.h/2-self.y
            self.reldist = self.dist/(rightPaddle.h/2)
            self.angle = self.reldist*(-135)


def showScore():
    leftScoreText = font.render("Score : " + str(scoreLeft), True, red)
    rightScoreText = font.render("Score : " + str(scoreRight), True, blue)

    display.blit(leftScoreText, (3*margin, 3*margin))
    display.blit(rightScoreText, (width/2 + 3*margin, 3*margin))

def gameOver():
    if scoreLeft == maxScore or scoreRight == maxScore:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_r:
                        reset()
            if scoreLeft == maxScore:
                playerWins = largeFont.render("Left Player Wins!", True, red)
            elif scoreRight == maxScore:
                playerWins = largeFont.render("Right Player Wins!", True, blue)

            display.blit(playerWins, (width/2 - 100, height/2))
            pygame.display.update()

def reset():
    global scoreLeft, scoreRight
    scoreLeft = 0
    scoreRight = 0
    root = Tk()
    root.title("MENU")
    temp=IntVar()
    b1=Button(root,text="vs. COMPUTER",command=COMP)
    Label(root, text='computer speed\n0-10').grid(column=3,row=1)
    e1 = Entry(root,textvariable=temp)
    e1.grid(column=5,row=1)
    b1.grid(column=1,row=1)
    b2=Button(root,text="vs. Player",command=multi)
    b2.grid(column=1,row=2)

    root.mainloop() 


def close():
    pygame.quit()
    sys.exit()

def multi():
    root.destroy()
    loop = True
    leftChange = 0
    rightChange = 0
    ball = Ball(yellow)
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_w:
                    leftChange = -1
                if event.key == pygame.K_s:
                    leftChange = 1
                if event.key == pygame.K_UP:
                    rightChange = -1
                if event.key == pygame.K_DOWN:
                    rightChange = 1
            if event.type == pygame.KEYUP:
                leftChange = 0
                rightChange = 0

        leftPaddle.move(leftChange)
        rightPaddle.move(rightChange)
        ball.move()
        ball.Collision() 
        
        display.fill(background)
        showScore()

        ball.show()
        leftPaddle.show()
        rightPaddle.show()

        boundary()

        gameOver()
        
        pygame.display.update()
        clock.tick(60)

def COMP():
    if temp.get() >=0 and temp.get() < 10:
        rightPaddle.paddleSpeed=temp.get()
    else:
        rightPaddle.paddleSpeed=4
    root.destroy()
    loop = True
    leftChange = 0
    rightChange = 0
    ball = Ball(yellow)
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_w:
                    leftChange = -1
                if event.key == pygame.K_s:
                    leftChange = 1
            if event.type == pygame.KEYUP:
                leftChange = 0

        leftPaddle.move(leftChange)

        if ball.y <= rightPaddle.y and ball.y >= rightPaddle.y+ rightPaddle.h:
                rightChange=0
        elif ball.y > rightPaddle.y:
                rightChange=1
        elif ball.y < rightPaddle.y:
                rightChange=-1

        rightPaddle.move(rightChange)

        ball.move()
        ball.Collision()
        
        display.fill(background)
        showScore()

        ball.show()
        leftPaddle.show()
        rightPaddle.show()

        boundary()

        gameOver()
        
        pygame.display.update()
        clock.tick(60)

root = Tk()
root.title("MENU")
temp=IntVar()
b1=Button(root,text="vs. COMPUTER",command=COMP)
Label(root, text='computer speed\n0-10').grid(column=3,row=1)
e1 = Entry(root,textvariable=temp)
e1.grid(column=5,row=1)
b1.grid(column=1,row=1)
b2=Button(root,text="vs. Player",command=multi)
b2.grid(column=1,row=2)

root.mainloop() 