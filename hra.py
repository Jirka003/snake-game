import pygame
import random
import sys
import os

pygame.init()

# ---------- RESOURCE PATH (FIXED) ----------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# ---------- OKNO ----------
WIDTH, HEIGHT = 960, 640
BLOCK = 64

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nejíst psa!")
clock = pygame.time.Clock()

# ---------- BARVY ----------
BG = (248, 244, 238)
PLAY_BG = (225, 215, 200)
PANEL = (180, 195, 180)
ACCENT = (120, 150, 120)
TEXT = (50, 50, 50)
WHITE = (255, 255, 255)

# ---------- FONT ----------
font = pygame.font.Font(resource_path("assets/font.ttf"), 24)
bigfont = pygame.font.Font(resource_path("assets/font.ttf"), 46)

# ---------- RYCHLOST ----------
BASE_FPS = 4
MAX_FPS = 10

# ---------- OBRÁZKY ----------
def load_img(path):
    img = pygame.image.load(resource_path(path)).convert_alpha()
    return pygame.transform.smoothscale(img, (BLOCK, BLOCK))

snake_head_img = load_img("assets/snake_head.png")
snake_body_img = load_img("assets/snake_body.png")
mouse_img = load_img("assets/mouse.png")
rat_img = load_img("assets/rat.png")
guinea_img = load_img("assets/guinea.png")
dog_img = load_img("assets/dog.png")

# ---------- TLAČÍTKO ----------
def draw_button(text, x, y, w, h):
    mx, my = pygame.mouse.get_pos()
    hover = x < mx < x + w and y < my < y + h

    color = ACCENT if hover else PANEL
    pygame.draw.rect(win, color, (x, y, w, h), border_radius=18)

    label = font.render(text, True, WHITE)
    win.blit(
        label,
        (x + w // 2 - label.get_width() // 2,
         y + h // 2 - label.get_height() // 2)
    )

    return hover

# ---------- FOOD ----------
class Food:
    def __init__(self, snake):
        self.spawn(snake)

    def spawn(self, snake):
        margin = BLOCK
        while True:
            self.x = random.randrange(margin, WIDTH - margin, BLOCK)
            self.y = random.randrange(margin + BLOCK, HEIGHT - margin, BLOCK)
            if (self.x, self.y) not in snake:
                break

        types = ["mouse"]*50 + ["rat"]*30 + ["guinea"]*15 + ["dog"]*5
        self.type = random.choice(types)

        self.image = {
            "mouse": mouse_img,
            "rat": rat_img,
            "guinea": guinea_img,
            "dog": dog_img
        }[self.type]

        self.points = {
            "mouse": 1,
            "rat": 2,
            "guinea": 3,
            "dog": -2
        }[self.type]

    def draw(self):
        win.blit(self.image, (self.x, self.y))

# ---------- MENU ----------
def menu():
    while True:
        win.fill(BG)

        title = bigfont.render("Pro Kačenku k Vánocům", True, TEXT)
        subtitle = font.render("Ovládání: WSAD", True, TEXT)
        subtitle2 = font.render("Pozor – nejez psa 🐶", True, TEXT)

        win.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
        win.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 180))
        win.blit(subtitle2, (WIDTH // 2 - subtitle2.get_width() // 2, 215))

        start_btn = draw_button("HRÁT", WIDTH // 2 - 100, 320, 200, 55)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_btn:
                return

# ---------- HRA ----------
def game():
    menu()

    snake = [(BLOCK * 5, BLOCK * 5)]
    dx, dy = BLOCK, 0
    score = 0
    fps = BASE_FPS

    food = Food(snake)

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and dy == 0:
                    dx, dy = 0, -BLOCK
                if event.key == pygame.K_s and dy == 0:
                    dx, dy = 0, BLOCK
                if event.key == pygame.K_a and dx == 0:
                    dx, dy = -BLOCK, 0
                if event.key == pygame.K_d and dx == 0:
                    dx, dy = BLOCK, 0

        head = (snake[0][0] + dx, snake[0][1] + dy)

        if head[0] < 0 or head[0] >= WIDTH or head[1] < BLOCK or head[1] >= HEIGHT:
            break
        if head in snake:
            break

        snake.insert(0, head)

        if head == (food.x, food.y):
            score += food.points
            food.spawn(snake)
            fps = min(MAX_FPS, BASE_FPS + score // 3)
        else:
            snake.pop()

        win.fill(PLAY_BG)
        pygame.draw.rect(win, PANEL, (0, 0, WIDTH, BLOCK))
        pygame.draw.line(win, ACCENT, (0, BLOCK), (WIDTH, BLOCK), 3)

        win.blit(font.render(f"Body: {score}", True, TEXT), (20, 18))
        win.blit(font.render(f"Rychlost: {fps}", True, TEXT), (800, 18))

        for i, part in enumerate(snake):
            if i == 0:
                angle = 0 if dx > 0 else 180 if dx < 0 else 90 if dy < 0 else -90
                img = pygame.transform.rotate(snake_head_img, angle)
                win.blit(img, part)
            else:
                win.blit(snake_body_img, part)

        food.draw()
        pygame.display.update()

    end_screen(score)

# ---------- KONEC ----------
def end_screen(score):
    while True:
        win.fill(BG)

        title = bigfont.render("Konec hry", True, TEXT)
        score_txt = font.render(f"Získané body: {score}", True, TEXT)

        win.blit(title, (WIDTH // 2 - title.get_width() // 2, 240))
        win.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, 300))

        restart_btn = draw_button("NOVÁ HRA", WIDTH // 2 - 100, 380, 200, 55)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and restart_btn:
                game()

game()
