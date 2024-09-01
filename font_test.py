import pygame
import sys

# Khởi tạo Pygame
pygame.init()
WIDTH = 750
HEIGHT = 600
# Thiết lập màn hình hiển thị
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sử dụng Font Tùy Chỉnh")

# Đường dẫn đến font của bạn (cập nhật đường dẫn chính xác)
font_path = 'Another Danger - Demo.otf'

# Tải font với kích thước 36
custom_font = pygame.font.Font(font_path, 70)

# Tạo một bề mặt văn bản từ font tùy chỉnh với màu đỏ
red_color = (52, 219, 130)  # Màu đỏ (RGB)
text_surface = custom_font.render("ZOMBIE EAT YOUR BRAIN", True, red_color)
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Điền màu nền
    window.fill((0, 0, 0))

    # Vẽ văn bản lên màn hình
    window.blit(text_surface, (text_rect))

    # Cập nhật màn hình
    pygame.display.flip()
