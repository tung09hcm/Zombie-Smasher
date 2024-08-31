import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Head Falling and Rotating Animation")

# Load the image
head_image = pygame.image.load('head.png').convert_alpha()

# Initial settings
x, y = 200, 100  # Starting position
y_bot = 500      # The y coordinate where the bottom of the image should stop
angle = 0        # Start with no rotation
max_angle = 60   # Maximum rotation angle
rotation_speed = 1  # Speed of rotation
falling_speed = 4   # Speed of falling

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate the image gradually until it reaches the max angle
    if angle < max_angle:
        angle += rotation_speed
        if angle > max_angle:
            angle = max_angle

    # Rotate the image by the current angle
    rotated_head = pygame.transform.rotate(head_image, angle)

    # Calculate the bottom position of the rotated image
    image_width, image_height = rotated_head.get_size()
    bottom_y_position = y + image_height

    # Move the image down if it hasn't reached the y_bot coordinate
    if bottom_y_position < y_bot:
        y += falling_speed

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the rotated image
    screen.blit(rotated_head, (x, y))

    # Refresh display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)


pygame.quit()
sys.exit()
