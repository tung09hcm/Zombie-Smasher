import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Explosion Animation")

# Load sprite sheet
sprite_sheet = pygame.image.load('explosion.png').convert_alpha()

# Explosion animation class
class ExplosionAnimation:
    def __init__(self, sprite_sheet, frame_width, frame_height, columns, rows):
        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.columns = columns
        self.rows = rows
        self.frames = self._load_frames()
        self.current_frame = 0
        self.animation_speed = 5  # Lower is faster
        self.counter = 0

    def _load_frames(self):
        frames = []
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
                frames.append(frame)
        return frames

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, surface, x, y):
        surface.blit(self.frames[self.current_frame], (x, y))

# Set up explosion animation
frame_width = 192
frame_height = 192
columns = 5  # Number of columns in the sprite sheet
rows = 2     # Number of rows in the sprite sheet

explosion = ExplosionAnimation(sprite_sheet, frame_width, frame_height, columns, rows)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update animation
    explosion.update()

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw explosion animation
    explosion.draw(screen, 300, 200)

    # Refresh display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
