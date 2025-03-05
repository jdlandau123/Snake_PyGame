import pygame
import random

pygame.init()
pygame.display.set_caption('Snake in Python!')
pygame.font.init()
running = True
clock = pygame.time.Clock()
elapsed_frames = 0

num_cols = 21 # odd number so that there's a definite middle
num_rows = 21
block_size = 36
screen = pygame.display.set_mode((num_cols * block_size, num_rows * block_size))

score = 0
direction = "right" # can be up, down, right, or left
apple_location = ( # apple always starts in the middle of the grid
  (num_cols - 1) / 2 * block_size,
  (num_rows - 1) / 2 * block_size
)
snake_head = [4 * block_size, 4 * block_size]
snake_locations = [
  snake_head,
  (snake_head[0], 3 * block_size),
  (snake_head[0], 2 * block_size),
  (snake_head[0], 1 * block_size),
  (snake_head[0], 0)
]

def is_game_over():
  if not 0 <= snake_head[0] < screen.get_width():
    return True
  if not 0 <= snake_head[1] < screen.get_height():
    return True
  if snake_head in snake_locations[1:]:
    return True
  return False

def render_game_over_screen():
  screen.fill("black")
  font = pygame.font.SysFont("Arial", 30)
  surface = font.render("Game Over!", False, "white")
  screen.blit(surface, (
    (screen.get_width() / 2) - (surface.get_width() / 2),
    (screen.get_height() / 2) - (surface.get_height() / 2)
  ))
  score_font = pygame.font.SysFont("Arial", 20)
  score_surface = score_font.render(f"Final Score: {score}", False, "white")
  screen.blit(score_surface, (
    (screen.get_width() / 2) - (score_surface.get_width() / 2),
    (screen.get_height() / 2) - (surface.get_height() / 2) + 50
  ))

if __name__ == "__main__":
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and direction != "down":
          direction = "up"
        if event.key == pygame.K_DOWN and direction != "up":
          direction = "down"
        if event.key == pygame.K_LEFT and direction != "right":
          direction = "left"
        if event.key == pygame.K_RIGHT and direction != "left":
          direction = "right"

    screen.fill("black")

    # draw the apple
    apple = pygame.Rect(apple_location[0], apple_location[1], block_size, block_size)
    pygame.draw.rect(screen, "red", apple)

    # draw the snake
    for loc in snake_locations:
      rect = pygame.Rect(loc[0], loc[1], block_size, block_size)
      pygame.draw.rect(screen, "green", rect)

    # draw the grid
    for i in range(block_size * num_rows): # num_rows and num_cols should be the same here
      if i % block_size == 0 and i > 0:
        pygame.draw.line(screen, "white", (i, 0), (i, screen.get_height()))
        pygame.draw.line(screen, "white", (0, i), (screen.get_width(), i))

    # draw score
    font = pygame.font.SysFont("Arial", 24)
    score_surface = font.render(f"Score: {score}", False, "white")
    screen.blit(score_surface, (0, 0))

    # move snake every other frame
    if elapsed_frames % 2 == 0:
      if direction == "right":
        new_head = [snake_head[0] + block_size, snake_head[1]]
      if direction == "left":
        new_head = [snake_head[0] - block_size, snake_head[1]]
      if direction == "up":
        new_head = [snake_head[0], snake_head[1] - block_size]
      if direction == "down":
        new_head = [snake_head[0], snake_head[1] + block_size]
      snake_head = new_head
      new_locs = [new_head]
      for i in range(1, len(snake_locations)):
        new_locs.append(snake_locations[i - 1])
      snake_locations = new_locs

    # check if apple was eaten
    if snake_head[0] == apple_location[0] and snake_head[1] == apple_location[1]:
      score += 1
      apple_location = ( # move the apple
        random.randint(0, num_cols - 1) * block_size,
        random.randint(0, num_rows - 1) * block_size
      )
      snake_locations.append(apple_location)

    # check if game over
    if is_game_over():
      # running = False
      render_game_over_screen()
        
    # flip frame
    pygame.display.update()
    clock.tick(30)
    elapsed_frames += 1
