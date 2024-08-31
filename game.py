import os
import random
import pygame
import threading
from os.path import join

pygame.init()
pygame.mixer.init()

sound_folder = 'zombie_sound'
sound_effects = {}
for file_name in os.listdir(sound_folder):
    if file_name.endswith('.ogg'):
        sound_name = os.path.splitext(file_name)[0]
        full_path = os.path.join(sound_folder, file_name)
        sound_effects[sound_name] = pygame.mixer.Sound(full_path)

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
def draw(window, background, bg_image,zombie,mobs, deaths, cursor_image, cursor_pos):
    # Xóa màn hình trước khi vẽ lại

    window.fill((255, 255, 255))  # Màu nền trắng hoặc màu nền phù hợp với trò chơi

    # Vẽ nền
    for title in background:
        window.blit(bg_image, title)

    for mob in mobs:
        mob.draw(window)

    for death in deaths:
        death.draw(window)
        death.update()

    # Vẽ con trỏ tùy chỉnh sau cùng để nằm trên các đối tượng khác
    x,y = cursor_pos
    window.blit(cursor_image, (x-32, y-32))

    # Cập nhật màn hình sau khi vẽ tất cả các đối tượng
    pygame.display.update()


class DeathAnimation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.max_angle = 45  # Giới hạn góc quay là 45 độ
        self.rotation_speed = 1
        self.falling_speed = 3
        self.timer = 0

        image_path = os.path.join('zombie', "head.png")
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))
        self.rotated_image = self.image

        image_width, image_height = self.image.get_size()
        self.bottom_y_position = self.y + image_height

    def update(self):
        self.timer += 1

        # Quay đầu lên đến góc tối đa
        if self.angle < self.max_angle:
            self.angle += self.rotation_speed
            if self.angle > self.max_angle:
                self.angle = self.max_angle
            self.rotated_image = pygame.transform.rotate(self.image, self.angle)

        # Khi đã quay đủ góc, bắt đầu rơi xuống
        if self.angle == self.max_angle:
            self.y += self.falling_speed

    def draw(self, window):
        # Tính toán vị trí để vẽ hình ảnh xoay
        rotated_rect = self.rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        window.blit(self.rotated_image, rotated_rect.topleft)
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
        self.alive = True

    def draw(self, window):
        if self.x < 0:
            self.x = 0
        elif self.x > (WIDTH - ZOMBIE_WIDTH):
            self.x = WIDTH - ZOMBIE_WIDTH
        if self.y < 0:
            self.y = 0

        if self.alive:
            window.blit(self.image, (self.x, self.y))
            window.blit(self.helmet.image, (self.x, self.y))
    def move(self):
        if self.alive:
            # Di chuyển mob theo trục x và trục y
            self.y += self.vel
            self.rect.topleft = (self.x, self.y)

    def update(self):
        if self.alive:
            num = random.randint(0, 4)
            image_name = "zombie" + str(num) + ".png"
            image_path = os.path.join('zombie', image_name)
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))
def spawn_random_zombie():
    x = random.randint(0, WIDTH - ZOMBIE_WIDTH)  # Tạo tọa độ x ngẫu nhiên trong giới hạn màn hình
    y = random.randint(0, 100)  # Tọa độ y ngẫu nhiên từ 0 đến 100
    vel = random.randint(1, 5)  # Tốc độ di chuyển ngẫu nhiên
    sprite = 0  # Sprite khởi đầu
    helmet_img_name = "null.png"  # Tên ảnh mũ ban đầu
    random_image = random.randint(0,2)
    if random_image == 0:
        helmet_img_name = "null.png"
    elif random_image == 1:
        helmet_img_name = "iron_helmet.png"
    else:
        helmet_img_name = "diamond_helmet.png"
    return Mob(x, y, vel, sprite, helmet_img_name)
def play_sound_and_wait(sound_name):
    sound_effects[sound_name].play()

def main(window):
    mobs = []
    run = True
    clock = pygame.time.Clock()
    background, bg_image = getBackground("Green.png")
    cursor_image = pygame.image.load("iron_axe.png")
    zombie = pygame.image.load("example/zombie.png")
    spawn_time = 0

    mobs = []
    zombie_sound = True
    check = True
    deaths = []

    while run:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        spawn_time += 1
        if spawn_time >= 120:
            so_luong = random.randint(1, 3)
            for _ in range(so_luong):
                mobs.append(spawn_random_zombie())
            spawn_time = 0
        if check:
            draw(window, background, bg_image, zombie, mobs, deaths, cursor_image, (mouse_x, mouse_y))

        # Cập nhật và xóa các zombie chết
        for death in deaths:
            death.update()

        # if len(mobs) > 0 and zombie_sound:
        #     zombie_sound = False
        #     thread1 = threading.Thread(target=lambda: play_sound_and_wait('Zombie_step1'))
        #     thread1.start()
        #
        #     thread1.join()
        #     zombie_sound = True

        # Xóa các zombie chết khi đã hoàn tất hiệu ứng
        deaths = [death for death in deaths if death.timer <= 20]

        for i, mob in enumerate(mobs):
            if mob.y >= HEIGHT:
                run = False
            if mob.rect.collidepoint(mouse_x, mouse_y):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:

                            cursor_image = pygame.image.load("iron_axe_swing.png")
                            mob.x = mob.x - 5
                            mob.y = mob.y - 10
                            if mob.helmet.durability > 0:
                                a = random.randint(1,2)
                                if a == 1:
                                    sound_effects['Zombie_hurt1'].play()
                                else:
                                    sound_effects['Zombie_hurt2'].play()
                                mob.helmet.durability -= 1
                                print("HIT!!! durability: " + str(mob.helmet.durability))
                                mob.helmet.update()
                            else:
                                print("1 hit and gone")
                                x = mob.x
                                y = mob.y
                                y_bot = y + ZOMBIE_HEIGHT
                                mob.alive = False
                                mobs.pop(i)
                                deaths.append(DeathAnimation(x, y))
                                sound_effects['Zombie_death'].play()
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            cursor_image = pygame.image.load("iron_axe.png")
            mob.sprite += 1
            if mob.sprite == 3:
                mob.move()
            if mob.sprite == 5:
                mob.update()
                mob.sprite = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cursor_image = pygame.image.load("iron_axe_swing.png")
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    cursor_image = pygame.image.load("iron_axe.png")

    black = (0, 0, 0)
    red = (255, 0, 0)
    font = pygame.font.SysFont(None, 100)
    text = font.render('YOU LOSE', True, red)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    while True:
        # Kiểm tra sự kiện để đóng cửa sổ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Tô nền màu đen
        window.fill(black)

        # Vẽ chữ "YOU LOSE" lên màn hình
        window.blit(text, text_rect)

        # Cập nhật màn hình
        pygame.display.flip()

if __name__ == "__main__":
    main(window)

