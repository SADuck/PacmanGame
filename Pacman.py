import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
PACMAN_RADIUS = 20
GHOST_RADIUS = 15
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
GAME_OVER_FONT = pygame.font.Font(None, 36)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Game")

# Initial positions for Pacman and ghosts
pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
ghosts = [(100, 200), (500, 300), (300, 100), (400, 400)]

# Randomize ghost speeds (between 1 and 3)
ghost_speeds = [random.uniform(1, 3) for _ in range(4)]

# Game state
game_over = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset game state here (reposition Pacman, ghosts, etc.)
                game_over = False
                pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
                ghosts = [(100, 200), (500, 300), (300, 100), (400, 400)]
                ghost_speeds = [random.uniform(1, 3) for _ in range(4)]

    if not game_over:
        # Calculate ghost movement towards Pacman
# After updating ghost positions
        # After updating ghost positions
        for i in range(4):
            ghost_x, ghost_y = ghosts[i]
            dx = pacman_x - ghost_x
            dy = pacman_y - ghost_y
            distance = math.sqrt(dx**2 + dy**2)

            # Normalize the direction vector
            if distance > 0:
                dx /= distance
                dy /= distance

            # Update ghost position with varying speed
            new_x, new_y = ghost_x + dx * ghost_speeds[i], ghost_y + dy * ghost_speeds[i]

            # Keep ghosts within screen boundaries
            new_x = max(GHOST_RADIUS, min(WIDTH - GHOST_RADIUS, new_x))
            new_y = max(GHOST_RADIUS, min(HEIGHT - GHOST_RADIUS, new_y))

            # Avoid ghost overlapping
            for j in range(4):
                if i != j:
                    other_ghost_x, other_ghost_y = ghosts[j]
                    other_distance = math.sqrt((new_x - other_ghost_x)**2 + (new_y - other_ghost_y)**2)
                    if other_distance < 2 * GHOST_RADIUS:
                        # Adjust ghost position to avoid overlap
                        overlap_correction = 2 * GHOST_RADIUS - other_distance
                        new_x += dx * overlap_correction * 0.5  # Reduce the correction factor
                        new_y += dy * overlap_correction * 0.5  # Reduce the correction factor

            ghosts[i] = (new_x, new_y)


        # Check for collisions with ghosts and Pacman
        for ghost_x, ghost_y in ghosts:
            if math.sqrt((pacman_x - ghost_x)**2 + (pacman_y - ghost_y)**2) < PACMAN_RADIUS + GHOST_RADIUS:
                game_over = True

    # Handle user input (arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x -= 5
    if keys[pygame.K_RIGHT]:
        pacman_x += 5
    if keys[pygame.K_UP]:
        pacman_y -= 5
    if keys[pygame.K_DOWN]:
        pacman_y += 5

    # Draw Pacman and ghosts
    screen.fill((0, 0, 0))  # Clear the screen
    pygame.draw.circle(screen, PACMAN_COLOR, (pacman_x, pacman_y), PACMAN_RADIUS)
    for ghost_x, ghost_y in ghosts:
        pygame.draw.circle(screen, GHOST_COLOR, (int(ghost_x), int(ghost_y)), GHOST_RADIUS)

    # Display game over screen
    if game_over:
        game_over_text = GAME_OVER_FONT.render("Game Over! Press R to restart.", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
