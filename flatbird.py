import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flatbird")

# Màu sắc và font chữ
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont(None, 40)

# Cài đặt chú chim
BIRD_WIDTH, BIRD_HEIGHT = 20, 15
bird_x = WIDTH // 4
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_height = -10

# Cài đặt ống
PIPE_WIDTH = 70
PIPE_GAP = 200
pipe_velocity = -4
pipe_list = []

# Tạo ống mới
def create_pipe():
    pipe_height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, pipe_height)
    bottom_pipe = pygame.Rect(WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)
    return top_pipe, bottom_pipe

# Kiểm tra va chạm
def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False

# Hiển thị điểm số
def draw_score(score):
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Khởi tạo game
clock = pygame.time.Clock()
score = 0
pipe_timer = 0
game_over = False

# Vòng lặp game
running = True
while running:
    screen.fill(WHITE)

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump_height
            if event.key == pygame.K_SPACE and game_over:
                bird_y = HEIGHT // 2
                bird_velocity = 0
                pipe_list.clear()
                score = 0
                game_over = False

    # Cập nhật vị trí chú chim
    if not game_over:
        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        
        # Tạo ống mới
        pipe_timer += 1
        if pipe_timer > 90:
            pipe_list.extend(create_pipe())
            pipe_timer = 0

        # Di chuyển và xóa ống
        for pipe in pipe_list:
            pipe.x += pipe_velocity
        pipe_list = [pipe for pipe in pipe_list if pipe.x > -PIPE_WIDTH]

        # Kiểm tra va chạm
        if check_collision(bird_rect, pipe_list) or bird_y > HEIGHT or bird_y < 0:
            game_over = True

        # Tăng điểm khi qua ống
        for pipe in pipe_list:
            if pipe.x == bird_x:
                score += 0.5

    # Vẽ chú chim và ống
    pygame.draw.rect(screen, BLACK, bird_rect)
    for pipe in pipe_list:
        pygame.draw.rect(screen, BLACK, pipe)

    # Hiển thị điểm số
    draw_score(int(score))

    # Hiển thị màn hình thua
    if game_over:
        game_over_text = FONT.render("Game Over! Press SPACE to Restart", True, BLACK)
        screen.blit(game_over_text, (20, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
