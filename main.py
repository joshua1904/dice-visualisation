# Example file showing a basic pygame "game loop"
import pygame
import random
import time
from screeninfo import get_monitors

pygame.mixer.init()
pygame.mixer.music.load("sounds/song.mp3")
winsound = pygame.mixer.Sound("sounds/coin.mp3")
fail_sound = pygame.mixer.Sound("sounds/fail.mp3")
# Setting the volume
pygame.mixer.music.set_volume(0.0)

# Start playing the song
pygame.mixer.music.play(-1)

SCREEN_WIDTH = get_monitors()[0].width
SCREEN_HEIGHT = get_monitors()[0].height
LINE_THICKNESS = int((SCREEN_HEIGHT / 100) * 0.6)
# pygame setup
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
MUSIC = False
clock = pygame.time.Clock()
running = True
COLORS = {0: "#4C78A8", 1: "#F58518", 2: "#E45756", 3: "#72B7B2"}
POSITIONS = [[0, 0, 0, 0]]
ROUND = 0
X_COORDINATE = 0
X_STEP = SCREEN_WIDTH / 9 - SCREEN_WIDTH / 200
Y_STEP = SCREEN_HEIGHT / 100
RESETS = 0
WINS = 0
pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', int(SCREEN_HEIGHT /30))
MAX_ROUNDS = 150



def toggle_music(music):
    if music:
        pygame.mixer.music.set_volume(0.0)
        return False
    else:
       pygame.mixer.music.set_volume(1.0)
       return True

def is_win(current_state: list):
    if current_state.count(current_state[0]) >= 3:
        return True
    if current_state.count(current_state[1]) >= 3:
        return True
    return False


def sim_round():
    line_1 = POSITIONS[-1][0] + random.randint(1, 6)
    line_2 = POSITIONS[-1][1] + random.randint(1, 6)
    line_3 = POSITIONS[-1][2] + random.randint(1, 6)
    line_4 = POSITIONS[-1][3] + random.randint(1, 6)
    POSITIONS.append([line_1, line_2, line_3, line_4])


def normalize_round(removed_list):
    remove_value = min(removed_list)
    for position in POSITIONS:
        position[0] -= remove_value
        position[1] -= remove_value
        position[2] -= remove_value
        position[3] -= remove_value


while running:
    text_surface = my_font.render(f'Wins: {WINS} rounds: {RESETS + WINS}', "#E8E8E8", "#E8E8E8")
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/ 2, SCREEN_HEIGHT / 100))
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_1:
                MUSIC = toggle_music(MUSIC)

    pygame.display.flip()
    if is_win(POSITIONS[-1]) and len(POSITIONS) != 1:
        WINS += 1
        POSITIONS = [[0, 0, 0, 0]]
        winsound.play()
        time.sleep(0.4)
        ROUND = 0
    sim_round()

    X_COORDINATE = 0
    screen.fill("#1A1A1A")
    screen.blit(text_surface, text_rect)
    for j in range(len(POSITIONS) - 1):
        for i in range(4):
            pygame.draw.line(screen, COLORS[i], (X_COORDINATE, POSITIONS[j][i] * Y_STEP),
                             (X_COORDINATE + X_STEP, POSITIONS[j + 1][i] * Y_STEP), LINE_THICKNESS)
        X_COORDINATE += X_STEP

    if len(POSITIONS) >= 10:
        x = POSITIONS.pop(0)
        normalize_round(x)

    ROUND += 1
    if ROUND == MAX_ROUNDS:
        fail_sound.play()
        POSITIONS = [[0, 0, 0, 0]]
        ROUND = 0
        RESETS += 1
        time.sleep(0.4)

    clock.tick(30)

pygame.quit()
