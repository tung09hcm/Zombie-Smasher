import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Platformer")
pygame.mouse.set_visible(False)  # Ẩn con trỏ mặc định

WIDTH = 750
HEIGHT = 600
FPS = 60

ZOMBIE_WIDTH = 53
ZOMBIE_HEIGHT = 84
HELMET_HEIGHT = 34

window = pygame.display.set_mode((WIDTH, HEIGHT))

def getBackground(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    titles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            titles.append(pos)

    return titles, image
def draw(window, background, bg_image,zombie,mobs, cursor_image, cursor_pos):
    # Xóa màn hình trước khi vẽ lại
    window.fill((255, 255, 255))  # Màu nền trắng hoặc màu nền phù hợp với trò chơi

    # Vẽ nền
    for title in background:
        window.blit(bg_image, title)

    for mob in mobs:
        # Vẽ zombie tại tọa độ (0,0)
        mob.draw(window)

    # Vẽ con trỏ tùy chỉnh sau cùng để nằm trên các đối tượng khác
    x,y = cursor_pos
    window.blit(cursor_image, (x-32, y-32))

    # Cập nhật màn hình sau khi vẽ tất cả các đối tượng
    pygame.display.update()

class Helmet:
    def __init__(self,x,y,image_name):
        self.x = x
        self.y = y
        self.image_name = image_name
        if self.image_name == "iron_helmet.png":
            self.type = "IRON"
            self.durability = 3
        elif self.image_name == "diamond_helmet.png":
            self.type = "DIAMOND"
            self.durability = 5
        else:
            self.durability = 0

        image_path = os.path.join('zombie', image_name)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (ZOMBIE_WIDTH, HELMET_HEIGHT))

    def update(self):
        image_path = os.path.join('zombie', self.image_name)
        if self.durability == 0:
            image_path = os.path.join('zombie', "null.png")
            self.image_name = "null.png"
        elif self.type == "IRON":
            if self.durability == 2:
                image_path = os.path.join('zombie', "iron_helmet0.png")
                self.image_name = "iron_helmet0.png"
            elif self.durability == 1:
                image_path = os.path.join('zombie', "iron_helmet1.png")
                self.image_name = "iron_helmet1.png"
        elif self.type == "DIAMOND":
            if self.durability == 3:
                image_path = os.path.join('zombie', "diamond_helmet0.png")
                self.image_name ="diamond_helmet0.png"
            elif self.durability == 1:
                image_path = os.path.join('zombie', "diamond_helmet1.png")
                self.image_name = "diamond_helmet1.png"
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (ZOMBIE_WIDTH, HELMET_HEIGHT))

class Mob:
    def __init__(self, x, y, vel, sprite, helmet_img_name):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.vel = vel  # Vận tốc di chuyển
        self.helmet = Helmet(x,y,helmet_img_name)

        image_path = os.path.join('zombie', "zombie0.png")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))

        self.rect = pygame.Rect(x, y,ZOMBIE_WIDTH, ZOMBIE_HEIGHT)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        window.blit(self.helmet.image, (self.x, self.y))

    def move(self):
        # Di chuyển mob theo trục x và trục y
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)

    def update(self):
        num = random.randint(0, 4)
        image_name = "zombie" + str(num) + ".png"
        image_path = os.path.join('zombie', image_name)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))

def main(window):
    mobs = []
    run = True
    clock = pygame.time.Clock()
    background, bg_image = getBackground("Green.png")
    cursor_image = pygame.image.load("iron_axe.png")
    zombie = pygame.image.load("example/zombie.png")


    mobs = [Mob(100, 100, 1,0, "null.png"),
            Mob(200, 150, 1,0, "diamond_helmet.png")]


    while run:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw(window, background, bg_image,zombie, mobs,cursor_image, (mouse_x, mouse_y))
        i = 0
        for mob in mobs:
            if mob.rect.collidepoint(mouse_x, mouse_y):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            cursor_image = pygame.image.load("iron_axe_swing.png")
                            if mob.helmet.durability > 0:
                                mob.helmet.durability -= 1
                                print("HIT!!! durability: " + str(mob.helmet.durability))
                                mob.helmet.update()
                            else:
                                # durability = 0
                                print("1 hit and gone")
                                # ============ ZOMBIE DEATH ANIMATION FUNCTION HERRE ============ #

                                # ============ DROP ITEM FUNCTION HERE ============ #

                                mobs.pop(i)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            cursor_image = pygame.image.load("iron_axe.png")


            mob.sprite += 1
            if mob.sprite == 3:
                mob.move()
            if mob.sprite == 5:
                mob.update()
                mob.sprite = 0
            i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cursor_image = pygame.image.load("iron_axe_swing.png")
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    cursor_image = pygame.image.load("iron_axe.png")


if __name__ == "__main__":
    main(window)
