import pygame
from pygame.locals import *
import sys

(w,h)=(800,500)						#スクリーンの大きさ
(x,y)=(w/2,400)	
SCREEN = Rect(100, 0, 700, 500)

pygame.init()  #pygameの初期化
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("戦闘機で倒せ！！")
bg = pygame.image.load("haikei.jpg").convert_alpha()
rect_bg = bg.get_rect()

class Flyer(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.x = x  #インスタンス変数らを定義
        self.y = y
        self.image = pygame.image.load(filename).convert_alpha()
        # self.img_rect = self.image.get_rect()
        w = self.image.get_width()
        h = self.image.get_height()
        self.rect = Rect(x, y, w, h)
        self.vx = vx
        self.vy = vy

    def draw(self, screen):
        screen.blit(self.image, self.rect) 

class Player(Flyer):
    def __init__(self, filename, x, y, vx, vy):
        super().__init__(filename, x, y, vx, vy)

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_LEFT]:
            self.rect.move_ip(-self.vx, 0)
        if pressed_key[pygame.K_RIGHT]:
            self.rect.move_ip(self.vx, 0)
        if pressed_key[pygame.K_UP]:
            self.rect.move_ip(0, -self.vy)
        if pressed_key[pygame.K_DOWN]:
            self.rect.move_ip(0, self.vy)   
        if self.y < -30 or self.y > h or self.x < -30 or self.x > w:
            pygame.sprite.Sprite.remove(self)

    def shoot(self, screen):
        class Bullet(object):  #objectは何？
            def __init__(self, x: int, y: int):
                self.bullet = Rect(x, y, 10, 20)  #弾の形

            def draw(self):
                pygame.draw.rect(screen, (255, 0, 0), self.bullet)  #数字は色
                tama_iti = self.bullet.left + self.bullet.right / 2
                return tama_iti

            def move(self, x: int=0, y: int=-5):  #動く方向
                self.bullet.move_ip(x, y)

            @property
            def is_destroy(self) -> bool:
                if self.bullet.x < -30 or self.bullet.y < - 30:
                    return True
                return False
        return Bullet(self.rect.x+33, self.rect.y)

class Enemy(Flyer):
    def __init__(self, filename, x, y, vx, vy):
        super().__init__(filename, x, y, vx, vy)

    def move(self):
        xy = []
        # img_rect = self.image.get_rect()
        # img_rect.move_ip(self.vx, self.vy)
        self.rect.move_ip(self.vx, self.vy)
        self.rect = self.rect.clamp(SCREEN)
        if self.rect.left < 110 or self.rect.right > 700:
            self.vx = -self.vx
        xy.append(self.rect.left)
        xy.append(self.rect.right)
        return xy
        # if img_rect.top < 0 or img_rect.bottom > 500:
        #     vy = -vy
        # self.rect.move_ip(self.vx, self.vy)
        # self.rect = self.rect.clamp(SCREEN)
        

def main():
    flag = 0
    player = Player("戦闘機.jpg", x, y, 5, 5)
    enemy1 = Enemy("monster06.png", 200, 200, 10, 0)
    enemy2 = Enemy("monster06.png", 100, 100, 10, 0)
    clock = pygame.time.Clock()
    bullet_list = []
    while 1:
        clock.tick(30)
        screen.fill((0, 0, 0))
        screen.blit(bg, rect_bg)
        player.move()
        enemy1.move()
        enemy2.move()
        #xy1 = enemy1.move()
        xy2 = enemy2.move()
        player.draw(screen)
        #enemy1.draw(screen)
        enemy2.draw(screen)
        if flag == 0:
            xy1 = enemy1.move()
            enemy1.draw(screen)
        if flag == 1:
            enemy1.kill()
        # 5,bullet_listの内容をfor in ループで回す。
        for bullet in bullet_list:
            bullet.move()
            bullet.draw()
            if bullet.draw() > xy1[0] and bullet.draw() < xy1[1]:
                flag = 1
        #リストからスクリーン範囲外のbulletをクリーンアップ
        bullet_list = list(filter(lambda x: not x.is_destroy, bullet_list))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 2,ショット：スペースキーを押下時に弾を発射
                if event.key == pygame.K_SPACE:
                    # 発射時にbullet_listに追加
                    bullet = player.shoot(screen)
                    # 4,リストにplayer.shootの戻り値である変数:bulletを追加
                    bullet_list.append(bullet)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
if __name__ == "__main__":
    main()

        
        