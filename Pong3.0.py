
'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Howard C Davis
Final Tk
'''

from tkinter import *
from tkinter import ttk

import pygame
import sys
import random


#Color
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
AQUA = 	(0,255,255)
MAGENTA = (255,0,255)
PURPLE = (128,0,128)

entity_color = WHITE
background = BLACK

#Player and enemy points
POINTP = 0
POINTE = 0
LOSE = 0
TEXT = ""
ES = 1  #Enemy speed to change
done = 0

class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Paddle(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        super(Paddle, self).__init__(x, y, width, height)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(entity_color)


class Player(Paddle):
    """The player controlled Paddle"""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)

        # How many pixels the Player Paddle should move on a given frame.
        self.y_change = 0
        self.x_change = 0
        # How many pixels the paddle should move each frame a key is pressed.
        self.y_dist = 5
        self.x_dist = 5

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_UP):
            self.y_change += -self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += self.y_dist

    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_UP):
            self.y_change += self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += -self.y_dist

    '''def MoveKeyLeft(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_RIGHT):
            self.x_change += -self.x_dist
        elif (key == pygame.K_LEFT):
            self.x_change += self.x_dist

    def MoveKeyRight(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_RIGHT):
            self.x_change += self.x_dist
        elif (key == pygame.K_LEFT):
            self.x_change += -self.x_dist'''

    def update(self):
        """
        Moves the paddle while ensuring it stays in bounds
        """
        # Moves it relative to its current location.
        self.rect.move_ip(self.x_change, self.y_change)

        # If the paddle moves off the screen, put it back on.
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height
        if self.rect.x > window_width - self.width:
            self.rect.x = window_width - self.width


class Enemy(Paddle):
    """
    AI controlled paddle, simply moves towards the ball
    and nothing else.
    """

    def __init__(self, x, y, width, height):
        super(Enemy, self).__init__(x, y, width, height)

        self.y_change = 2

    def update(self):
        """
        Moves the Paddle while ensuring it stays in bounds
        """
        # Moves the Paddle up if the ball is above,
        # and down if below.
        if ball.rect.y < self.rect.y:
            self.rect.y -= self.y_change+ES+1
        elif ball.rect.y > self.rect.y:
            self.rect.y += self.y_change+ES+1

        # The paddle can never go above the window since it follows
        # the ball, but this keeps it from going under.
        if self.rect.y + self.height > window_height:
            self.rect.y = window_height - self.height


class Ball(Entity):
    """
    The ball!  Moves around the screen.
    """

    def __init__(self, x, y, width, height):
        super(Ball, self).__init__(x, y, width, height)

        self.image = pygame.Surface([width, height])
        self.image.fill(entity_color)

        self.x_direction = 1
        # Positive = down, negative = up
        self.y_direction = 1
        # Current speed.
        self.speed = 4

    def update(self):
        # Move the ball!
        self.rect.move_ip(self.speed * self.x_direction,
                          self.speed * self.y_direction)

        # Keep the ball in bounds, and make it bounce off the sides.
        if self.rect.y < 0:
            self.y_direction *= -1
        elif self.rect.y > window_height - 20:
            self.y_direction *= -1
        if self.rect.x < 0:
            self.x_direction *= -1
        elif self.rect.x > window_width - 20:
            self.x_direction *= -1


def PlayerScore():
    fontObj = pygame.font.SysFont('comicsansms', 40)
    textSurfaceObj = fontObj.render(str(POINTP), True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (100,30)

    return textSurfaceObj, textRectObj

def EnemyScore():
    fontObj = pygame.font.SysFont('comicsansms', 40)
    textSurfaceObj = fontObj.render(str(POINTE), True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = ((window_width)-100,30)

    return textSurfaceObj, textRectObj

def LoseScreen(text):
    fontObj = pygame.font.SysFont('comicsansms', 40)

    textSurfaceObjL = fontObj.render(text, True, WHITE)
    textRectObjL = textSurfaceObjL.get_rect()
    textRectObjL.center = ((window_width/2),100)

    textSurfaceObj1 = fontObj.render(str(POINTP), True, WHITE)
    textRectObj1 = textSurfaceObj1.get_rect()
    textRectObj1.center = ((window_width / 2)-120, 200)

    textSurfaceObj2 = fontObj.render(str(POINTE), True, WHITE)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = ((window_width / 2) + 120, 200)

    textSurfaceObj3 = fontObj.render("-", True, WHITE)
    textRectObj3 = textSurfaceObj3.get_rect()
    textRectObj3.center = ((window_width / 2), 200)

    return textSurfaceObjL, textRectObjL, textSurfaceObj1, textRectObj1, textSurfaceObj2, textRectObj2, textSurfaceObj3, textRectObj3

def UserName():
    top = Tk()
    top.title("About")
    top.minsize(width=200, height=150)
    top.resizable(width=FALSE, height=FALSE)
    msg = Message(top, text='UserName:')
    #msg2 = Text()
    msg.pack()
    #msg2.pack()
    #button = Button(top, text="Next")  #command =
    #button.pack()


def top10(text):
    global done

    Open = open("Scores.txt","r")
    scores = []
    ShowScores = []
    Show = []
    for i in Open:
        number = i.replace('\n','')
        scores.append(number)
    Open.close()

    Open = open("Scores.txt","w")
    for i in scores:
        if POINTP > int(i):
            if done != 1:
                Open.write(str(POINTP) + '\n')
                ShowScores.append(POINTP)
                done += 1
            if done == 1:
                Open.write(i + '\n')
                ShowScores.append(i)
            if len(ShowScores) == 10:
                break
        else:
            Open.write(str(i) + '\n')
            ShowScores.append(i)

    Open.close()

    for i in ShowScores:
        Show.append(str(i)+'\n')

    fontObj = pygame.font.SysFont('comicsansms', 40)

    textSurfaceObjL = fontObj.render(text, True, WHITE)
    textRectObjL = textSurfaceObjL.get_rect()
    textRectObjL.center = ((window_width / 2), 100)

    textSurfaceObjP = fontObj.render('Your score is %s' % POINTP, True, WHITE)
    textRectObjP = textSurfaceObjP.get_rect()
    textRectObjP.center = ((window_width / 2), 150)

    textSurfaceObj2 = fontObj.render("Top Scores -", True, WHITE)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = ((window_width / 2), 250)

    print(ShowScores)

    textSurfaceObj3 = fontObj.render(str(ShowScores), True, WHITE)
    textRectObj3 = textSurfaceObj3.get_rect()
    textRectObj3.center = ((window_width / 2), 350)

    return textSurfaceObjL, textRectObjL, textSurfaceObjP, textRectObjP, textSurfaceObj2, textRectObj2, textSurfaceObj3, textRectObj3



pygame.init()

window_width = 1500
window_height = 700
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

ball = Ball(window_width / 2, window_height / 2, 20, 20)
player = Player(20, window_height / 2, 20, 70)
enemy = Enemy(window_width - 40, window_height / 2, 20, 70)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(ball)
all_sprites_list.add(player)
all_sprites_list.add(enemy)


while True:
    # Event processing here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player.MoveKeyDown(event.key)
            '''player.MoveKeyRight(event.key)'''
        elif event.type == pygame.KEYUP:
            player.MoveKeyUp(event.key)
            '''player.MoveKeyLeft(event.key)'''

    if LOSE == 0:
        #Checks if the ball has hit the player or has hit the side of the screen
        for ent in all_sprites_list:
            ent.update()

        if ball.rect.x <= player.rect.x+15 and ball.rect.y >= player.rect.y - 5 and ball.rect.y <= player.rect.y + 70:
            ball.x_direction *= -1
            ball.speed += .01
            enemy.y_change += .1
            player.y_change -= .01
            POINTP += 1

            if ball.rect.y >= player.rect.y and ball.rect.y <= player.rect.y + 20:
                ball.y_direction = 1
                ball.y_direction *= -1
                ES = 1
            if ball.rect.y >= player.rect.y + 20 and ball.rect.y <= player.rect.y + 50:
                ball.y_direction = 1
                r = random.randrange(2)
                if r == 0:
                    ball.y_direction *= -.5
                    ES = .5
                    print(ES)
                if r == 1:
                    ball.y_direction *= .5
                    ES = .5
                    #print(ES)
            if ball.rect.y >= player.rect.y + 50 and ball.rect.y <= player.rect.y + 70:
                ball.y_direction = 1
                ball.y_direction *= 1
                ES = 1

        if ball.rect.x <= player.rect.x:
            #POINTE += 1
            R = random.randrange(1,10)
            #print(R)
            ball.rect.x = window_width / 2
            ball.rect.y = window_height / R

            enemy.y_change = 2
            if POINTE == 1:
                LOSE = 1
                TEXT = "You Lose!"

        if ball.rect.x >= enemy.rect.x-15 and ball.rect.y >= enemy.rect.y - 5 and ball.rect.y <= enemy.rect.y + 70:
            ball.x_direction *= -1
            ball.speed += .01
            enemy.y_change += .1
            player.y_change -= .01
            #print(enemy.y_change)
            POINTE += 1

            if ball.rect.y >= enemy.rect.y and ball.rect.y <= enemy.rect.y + 20:
                ball.y_direction = 1
                ball.y_direction *= -1
                ES = 1
            if ball.rect.y >= enemy.rect.y + 20and ball.rect.y <= enemy.rect.y + 50:
                ball.y_direction = 1
                r = random.randrange(2)
                if r == 0:
                    ball.y_direction *= -.5
                    ES = .5
                    #print(ES)
                if r == 1:
                    ball.y_direction *= .5
                    ES = .5
                    #print(ES)
            if ball.rect.y >= enemy.rect.y + 50 and ball.rect.y <= enemy.rect.y + 70:
                ball.y_direction = 1
                ball.y_direction *= 1
                ES = 1

        if ball.rect.x >= enemy.rect.x:
            ball.rect.x = window_width / 2
            ball.rect.y = window_height / 2
            enemy.y_change = 2
            POINTP += 1

            if POINTP == 10:
                LOSE = 1
                TEXT = "You Win!"

        screen.fill(background)

        Text = EnemyScore()
        Surface = Text[0]
        Rect = Text[1]
        screen.blit(Surface, Rect)

        Text = PlayerScore()
        Surface = Text[0]
        Rect = Text[1]
        screen.blit(Surface, Rect)

        all_sprites_list.draw(screen)

        pygame.display.flip()

    elif LOSE == 1:
        screen.fill(background)

        '''Text = LoseScreen(TEXT)

        SurfaceL = Text[0]
        RectL = Text[1]
        Surface1 = Text[2]
        Rect1 = Text[3]
        Surface2 = Text[4]
        Rect2 = Text[5]
        Surface3 = Text[6]
        Rect3 = Text[7]
        screen.blit(SurfaceL, RectL)
        screen.blit(Surface1, Rect1)
        screen.blit(Surface2, Rect2)
        screen.blit(Surface3, Rect3)'''

        #UserName()

        Text = top10(TEXT)

        SurfaceL = Text[0]
        RectL = Text[1]
        Surface1 = Text[2]
        Rect1 = Text[3]
        Surface2 = Text[4]
        Rect2 = Text[5]
        Surface3 = Text[6]
        Rect3 = Text[7]

        screen.blit(SurfaceL, RectL)
        screen.blit(Surface1, Rect1)
        screen.blit(Surface2, Rect2)
        screen.blit(Surface3, Rect3)


        pygame.display.flip()

    clock.tick(60)