import pygame
from pygame.locals import *
import sys

SCR_WIDTH, SCR_HEIGHT = 640, 480
pygame.init()
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption("画像の移動と跳ね返り処理")

vx = 2
vy = 0

clock = pygame.time.Clock()

img = pygame.image.load("ピカチュウ.png").convert_alpha()
img_rect = img.get_rect()

while True:
    clock.tick(60)

    img_rect.move_ip(vx, vy)
    print(img_rect.left)
    if img_rect.left < 0 or img_rect.right > SCR_WIDTH:
        vx = -vx
    if img_rect.top < 0 or img_rect.bottom > SCR_HEIGHT:
        vy = -vy
    screen.fill((0,0,255))
    screen.blit(img, img_rect)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE: sys.exit()
