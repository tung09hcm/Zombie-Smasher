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
class Mob:
    def __init__(self, x, y, image_name, vel, sprite):
        self.x = x
        self.y = y
        self.image_name = image_name
        self.sprite = sprite
        self.vel = vel  # Vận tốc di chuyển

        image_path = os.path.join('zombie', image_name)
        self.image = pygame.image.load(image_path)
        original_width, original_height = self.image.get_size()
        new_width = int(original_width / 2)
        new_height = int(original_height / 2)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect = pygame.Rect(x, y,new_width,new_height)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        # Di chuyển mob theo trục x và trục y
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)

    def update(self):
        num = random.randint(0, 4)
        self.image_name = "zombie" + str(num) + ".png"
        image_path = os.path.join('zombie', self.image_name)
        self.image = pygame.image.load(image_path)
        original_width, original_height = self.image.get_size()
        new_width = int(original_width / 2)
        new_height = int(original_height / 2)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

def main(window):
    mobs = []
    run = True
    clock = pygame.time.Clock()
    background, bg_image = getBackground("Green.png")
    cursor_image = pygame.image.load("iron_axe.png")
    zombie = pygame.image.load("zombie.png")
    mobs = [Mob(100, 100, "zombie0.png", 1,0), Mob(200, 150, "zombie1.png", 1,0)]
    while run:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw(window, background, bg_image,zombie, mobs,cursor_image, (mouse_x, mouse_y))

        for mob in mobs:

            if mob.rect.collidepoint(mouse_x, mouse_y):
                print("CATCH ==>")
                print("=========")
            mob.sprite += 1
            if mob.sprite == 3:
                mob.move()
            if mob.sprite == 5:
                mob.update()
                mob.sprite = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    cursor_image = pygame.image.load("iron_axe_swing.png")
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    cursor_image = pygame.image.load("iron_axe.png")


if __name__ == "__main__":
    main(window)
