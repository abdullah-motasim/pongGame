import sys
import pygame
from config import *


class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((600, 600))
        self.font = pygame.font.SysFont('Comic Sans MS', 42)
        self.text = self.font.render("0 : 0", False, WHITE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.score1 = 0
        self.score2 = 0
        self.winner = 0

        # Players
        self.player_x1 = x1
        self.player_x2 = x2
        self.player_y1 = y1
        self.player_y2 = y2
        self.y1_change = 0
        self.y2_change = 0

        # Ball
        self.ballx = ballx
        self.bally = bally
        self.ballSpeed = BallSpeed
        self.x_change = 0
        self.y_change = 0
        self.xd = -1
        self.yd = -1

    def main(self):
        self.check_win()
        self.events()
        self.update()
        self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.y1_change = 0
        self.y2_change = 0
        self.movement()

        self.player_y1 += self.y1_change
        self.player_y2 += self.y2_change

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (x1, self.player_y1, player_width, player_height))
        pygame.draw.rect(self.screen, WHITE, (x2, self.player_y2, player_width, player_height))
        pygame.draw.rect(self.screen, WHITE, (self.ballx, self.bally, ball_width, ball_height))
        self.text = self.font.render(str(self.score1) + " : " + str(self.score2), False, WHITE)
        self.screen.blit(self.text, (font_width, font_height))
        pygame.display.update()

    def check_win(self):
        if self.score1 == 10:
            self.winner = 1
            self.running = False

        if self.score2 == 10:
            self.winner = 2
            self.running = False

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player_y2 - 10 > 0:
            self.y2_change -= PlayerSpeed
        if keys[pygame.K_DOWN] and self.player_y2 + player_height + 10 < height:
            self.y2_change += PlayerSpeed
        if keys[pygame.K_w] and self.player_y1 - 10 > 0:
            self.y1_change -= PlayerSpeed
        if keys[pygame.K_s] and self.player_y1 + player_height + 10 < height:
            self.y1_change += PlayerSpeed
        self.collision()
        self.ballx += self.ballSpeed * self.xd
        self.bally += self.ballSpeed * self.yd

    def collision(self):
        # Ball and wall collision
        if self.bally < 0 or self.bally + ball_height > height:
            self.yd *= -1
        if self.ballx <= 0:
            self.score2 += 1
            self.ballx = ballx
            self.xd *= -1
        if self.ballx + ball_width >= height:
            self.score1 += 1
            self.ballx = ballx
            self.xd *= -1

        # Ball and paddle collision
        if self.player_x1 < self.ballx < self.player_x1 + player_width and self.player_y1 < self.bally < self.player_y1 + player_height:
            self.ballx = self.ballx
            self.bally = self.bally
            self.xd *= -1
            # self.ballSpeed = 8
        if self.player_x2 < self.ballx + ball_height < self.player_x2 + player_width and self.player_y2 < self.bally < self.player_y2 + player_height:
            self.ballx = self.ballx
            self.bally = self.bally
            self.xd *= -1
            # self.ballSpeed = 3

    def gameover_screen(self):
        if self.winner == 1:
            self.screen.fill(BLACK)
            self.text = self.font.render("Player 1 Wins!", False, WHITE)
            self.screen.blit(self.text, (gameover_width, gameover_height))
            pygame.display.update()

        if self.winner == 2:
            self.screen.fill(BLACK)
            self.text = self.font.render("Player 2 Wins!", False, WHITE)
            self.screen.blit(self.text, (gameover_width, gameover_height))
            pygame.display.update()


g = Game()

while g.running:
    g.main()

g.gameover_screen()
gameover_showing = True

while gameover_showing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover_showing = False
        else:
            g.gameover_screen()

pygame.quit()
sys.exit()
