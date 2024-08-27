import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rotate Image on Click")

# Tải hình ảnh
image = pygame.image.load("iron_axe.png")  # Thay "your_image.png" bằng đường dẫn đến hình ảnh của bạn
image_rect = image.get_rect(center=(screen_width // 2, screen_height // 2))

# Góc xoay ban đầu
angle = 0
rotate = False

# Vòng lặp chính
count = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra nếu nhấp chuột vào hình ảnh
            if image_rect.collidepoint(event.pos):
                rotate = not rotate

    # Xoay hình ảnh nếu đã được nhấp
    if rotate:
        angle += 10  # Thay đổi góc xoay, bạn có thể tùy chỉnh tốc độ xoay ở đây
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=image_rect.center)
    else:
        rotated_image = image
        rotated_rect = image_rect
    count += 1
    if count == 300:
        count = 0
        rotate = not rotate
    print(count)
    # Vẽ màn hình
    screen.fill((255, 255, 255))
    screen.blit(rotated_image, rotated_rect)
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Giới hạn FPS
