import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mob Spawner with Progress Bar and Notification")

# Định nghĩa các màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PROGRESS_BAR_COLOR = (0, 128, 255)
PROGRESS_BAR_BG_COLOR = (200, 200, 200)
COLORS = [RED, GREEN, BLUE]

# Thiết lập FPS (Frames Per Second)
FPS = 60
clock = pygame.time.Clock()

# Định nghĩa thời gian và thông số thanh tiến trình
PROGRESS_BAR_WIDTH = 300
PROGRESS_BAR_HEIGHT = 30
PROGRESS_BAR_X = (WIDTH - PROGRESS_BAR_WIDTH) // 2
PROGRESS_BAR_Y = HEIGHT - 50
PROGRESS_TIME = 60  # Tổng thời gian để đi hết thanh tiến trình (giây)
start_time = pygame.time.get_ticks()  # Lấy thời gian bắt đầu (milliseconds)

# Khởi tạo font cho thông báo
font = pygame.font.SysFont('Arial', 30)

# Định nghĩa class Mob
class Mob:
    def __init__(self, x, y, size, color, vel):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.vel = vel  # Vận tốc di chuyển
        self.rect = pygame.Rect(x, y, size, size)  # Tạo một Rect để kiểm tra va chạm

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    def move(self):
        # Di chuyển mob theo trục x và trục y
        self.x += self.vel[0]
        self.y += self.vel[1]

        # Cập nhật vị trí của Rect theo vị trí mob
        self.rect.topleft = (self.x, self.y)

        # Đổi hướng nếu chạm vào biên
        if self.x <= 0 or self.x + self.size >= WIDTH:
            self.vel[0] = -self.vel[0]
        if self.y <= 0 or self.y + self.size >= HEIGHT:
            self.vel[1] = -self.vel[1]

# Hàm vẽ thanh tiến trình
def draw_progress_bar(window, current_time, start_time):
    elapsed_time = (current_time - start_time) / 1000  # Chuyển đổi sang giây
    progress_ratio = min(elapsed_time / PROGRESS_TIME, 1)  # Tính tỷ lệ đã hoàn thành

    # Vẽ thanh nền
    pygame.draw.rect(window, PROGRESS_BAR_BG_COLOR,
                     (PROGRESS_BAR_X, PROGRESS_BAR_Y, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT))

    # Vẽ thanh tiến trình
    progress_width = int(PROGRESS_BAR_WIDTH * progress_ratio)
    pygame.draw.rect(window, PROGRESS_BAR_COLOR,
                     (PROGRESS_BAR_X, PROGRESS_BAR_Y, progress_width, PROGRESS_BAR_HEIGHT))

# Hàm vẽ cửa sổ game
def draw_window(mobs, current_time, start_time, message=None):
    WINDOW.fill(WHITE)  # Làm sạch màn hình bằng màu trắng
    for mob in mobs:
        mob.draw(WINDOW)
    draw_progress_bar(WINDOW, current_time, start_time)  # Vẽ thanh tiến trình

    # Vẽ thông báo nếu có
    if message:
        text_surface = font.render(message, True, BLACK)
        WINDOW.blit(text_surface, (20, 20))

    pygame.display.update()

# Hàm chính của game
def main():
    mobs = []  # Danh sách các mob
    run = True
    message = None

    while run:
        clock.tick(FPS)  # Giới hạn FPS
        current_time = pygame.time.get_ticks()  # Thời gian hiện tại (milliseconds)
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy vị trí con trỏ chuột

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Sinh ra một mob mới khi nhấn phím SPACE
                    x = random.randint(0, WIDTH - 50)
                    y = random.randint(0, HEIGHT - 50)
                    size = random.randint(20, 50)
                    color = random.choice(COLORS)
                    vel = [random.choice([-2, 2]), random.choice([-2, 2])]
                    mob = Mob(x, y, size, color, vel)
                    mobs.append(mob)

        # Cập nhật và di chuyển các mob
        for mob in mobs:
            mob.move()
            # Kiểm tra nếu con trỏ chuột đang ở trong Rect của mob
            if mob.rect.collidepoint(mouse_x, mouse_y):
                message = "Con trỏ chạm vào mob!"
                break
        else:
            message = None  # Xóa thông báo nếu không có va chạm

        # Vẽ cửa sổ game
        draw_window(mobs, current_time, start_time, message)

    pygame.quit()

if __name__ == "__main__":
    main()
