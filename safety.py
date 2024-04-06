import pygame
import random

pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Настройки игры
player_size = 50
enemy_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size]
enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]
SPEED = 10

# Переменные игры
score = 0
game_over = False
clock = pygame.time.Clock()


# Класс игрока
class Player:
    def __init__(self, position):
        self.position = position

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.position[0], self.position[1], player_size, player_size))


# Класс врага
class Enemy:
    def __init__(self, position):
        self.position = position

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], enemy_size, enemy_size))


# Создаем объекты
player = Player(player_pos)


# Функция обновления позиции врагов
def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


# Функция столкновения
def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


# Функция обнаружения столкновения
def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False


# Игровой цикл
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            x = player.position[0]
            y = player.position[1]
            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size

            player.position = [x, y]

    screen.fill((0, 0, 0))

    # Обновляем и рисуем врагов
    if len(enemy_list) < 10 and random.randint(0, 20) < 1:
        enemy_list.append([random.randint(0, SCREEN_WIDTH - enemy_size), 0])

    score = update_enemy_positions(enemy_list, score)
    for pos in enemy_list:
        enemy = Enemy(pos)
        enemy.draw(screen)

    # Столкновение
    if collision_check(enemy_list, player.position):
        game_over = True
        break

    player.draw(screen)

    pygame.display.update()

    clock.tick(30)

print("Score:", score)
pygame.quit()