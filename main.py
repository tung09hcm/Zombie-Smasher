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
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))
RESTRICTED_RECT = pygame.Rect(200, 150, 30, 30)


zombie_x = 0
zombie_y = 0

def restrictMousePosition(mouse_pos, restricted_rect):
    x, y = mouse_pos
    check = False
    # Kiểm tra nếu chuột đang nằm trong vùng bị chặn
    if restricted_rect.collidepoint(x, y):
        check = True
        # Đẩy chuột ra khỏi vùng bị chặn
        if x < restricted_rect.left:
            x = restricted_rect.left - 30
        elif x > restricted_rect.right:
            x = restricted_rect.right + 30
        if y < restricted_rect.top:
            y = restricted_rect.top - 30
        elif y > restricted_rect.bottom:
            y = restricted_rect.bottom + 30
    if check:
        print("IN RESTRICTED AREA")
        print("==================")

    return x, y, check


def getBackground(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    titles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            titles.append(pos)

    return titles, image


def draw(window, background, bg_image,zombie, cursor_image, cursor_pos):
    # Xóa màn hình trước khi vẽ lại
    window.fill((255, 255, 255))  # Màu nền trắng hoặc màu nền phù hợp với trò chơi

    # Vẽ nền
    for title in background:
        window.blit(bg_image, title)

    # Vẽ vùng hitbox (màu đỏ)
    pygame.draw.rect(window, (255, 0, 0), RESTRICTED_RECT)
    window.blit(zombie, (zombie_x,zombie_y))

    # Vẽ con trỏ tùy chỉnh sau cùng để nằm trên các đối tượng khác
    x,y = cursor_pos
    window.blit(cursor_image, (x-32, y-32))

    # Cập nhật màn hình sau khi vẽ tất cả các đối tượng
    pygame.display.update()


def main(window):
    global zombie_x, zombie_y

    clock = pygame.time.Clock()
    background, bg_image = getBackground("Green.png")
    cursor_image = pygame.image.load("iron_axe.png")
    zombie = pygame.image.load("zombie.png")
    # Lấy kích thước hiện tại của ảnh
    original_width, original_height = zombie.get_size()

    # Tính toán kích thước mới (nhỏ hơn 1.5 lần)
    new_width = int(original_width / 2)
    new_height = int(original_height / 2)

    # Thay đổi kích thước ảnh
    zombie = pygame.transform.scale(zombie, (new_width, new_height))
    run = True

    while run:
        clock.tick(FPS)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        restricted_x, restricted_y, check = restrictMousePosition((mouse_x, mouse_y), RESTRICTED_RECT)

        # Kiểm tra và giới hạn vị trí chuột
        # if check:
        #    pygame.mouse.set_pos((restricted_x, restricted_y))

        # Vẽ tất cả mọi thứ (nền, vùng bị chặn, con trỏ)
        draw(window, background, bg_image,zombie, cursor_image, (mouse_x, mouse_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    cursor_image = pygame.image.load("iron_axe_swing.png")
                    zombie = pygame.image.load("zombie_head.png")
                    # Lấy kích thước hiện tại của ảnh
                    original_width, original_height = zombie.get_size()

                    # Tính toán kích thước mới (nhỏ hơn 1.5 lần)
                    new_width = int(original_width / 2)
                    new_height = int(original_height / 2)

                    # Thay đổi kích thước ảnh
                    zombie = pygame.transform.scale(zombie, (new_width, new_height))
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    cursor_image = pygame.image.load("iron_axe.png")

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
