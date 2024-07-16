import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GOLD = (255, 215, 0)  # Color for the super block

# Pastel color themes
THEMES = {
    "Spring": {
        "background": (255, 240, 245),  # Light Pink
        "snake": (144, 238, 144),       # Light Green
        "food": (255, 182, 193),        # Light Pink
        "text": (70, 130, 180)          # Steel Blue
    },
    "Summer": {
        "background": (255, 253, 208),  # Light Yellow
        "snake": (135, 206, 250),       # Light Sky Blue
        "food": (255, 160, 122),        # Light Salmon
        "text": (46, 139, 87)           # Sea Green
    },
    "Autumn": {
        "background": (255, 228, 196),  # Bisque
        "snake": (210, 180, 140),       # Tan
        "food": (221, 160, 221),        # Plum
        "text": (205, 92, 92)           # Indian Red
    },
    "Winter": {
        "background": (240, 248, 255),  # Alice Blue
        "snake": (176, 224, 230),       # Powder Blue
        "food": (255, 192, 203),        # Pink
        "text": (70, 130, 180)          # Steel Blue
    }
}

# Snake properties
snake_block = 20

# Initialize clock
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

def draw_grid():
    for x in range(0, width, snake_block):
        pygame.draw.line(window, GRAY, (x, 0), (x, height))
    for y in range(0, height, snake_block):
        pygame.draw.line(window, GRAY, (0, y), (width, y))

def our_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(window, color, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0, size="normal"):
    if size == "normal":
        mesg = font.render(msg, True, color)
    elif size == "small":
        mesg = small_font.render(msg, True, color)
    text_rect = mesg.get_rect(center=(width/2, height/2 + y_displace))
    window.blit(mesg, text_rect)

def draw_button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            return action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))
    
    text = small_font.render(msg, True, BLACK)
    text_rect = text.get_rect(center=((x+(w/2)), (y+(h/2))))
    window.blit(text, text_rect)

def game_settings():
    settings = {"speed": 15, "show_grid": False, "theme": "Spring"}
    setting_selected = False
    while not setting_selected:
        window.fill(THEMES[settings["theme"]]["background"])
        message("Game Settings", THEMES[settings["theme"]]["text"], -220)
        
        button_width = 120
        button_height = 50
        button_spacing = 20

        # Speed buttons (centered)
        speed_total_width = 3 * button_width + 2 * button_spacing
        speed_start_x = (width - speed_total_width) // 2
        y_position = height // 2 - 120

        if draw_button("Slow", speed_start_x, y_position, button_width, button_height, WHITE, GRAY, lambda: {"speed": 10}):
            settings.update({"speed": 10})
        if draw_button("Medium", speed_start_x + button_width + button_spacing, y_position, button_width, button_height, WHITE, GRAY, lambda: {"speed": 15}):
            settings.update({"speed": 15})
        if draw_button("Fast", speed_start_x + 2 * (button_width + button_spacing), y_position, button_width, button_height, WHITE, GRAY, lambda: {"speed": 20}):
            settings.update({"speed": 20})
        
        # Grid button
        y_position += button_height + button_spacing
        grid_text = "Show Grid" if not settings["show_grid"] else "Hide Grid"
        if draw_button(grid_text, width // 2 - button_width // 2, y_position, button_width, button_height, WHITE, GRAY, lambda: {"show_grid": not settings["show_grid"]}):
            settings["show_grid"] = not settings["show_grid"]
        
        # Theme buttons (centered)
        y_position += button_height + button_spacing
        theme_buttons = ["Spring", "Summer", "Autumn", "Winter"]
        theme_total_width = 4 * button_width + 3 * button_spacing
        theme_start_x = (width - theme_total_width) // 2

        for i, theme in enumerate(theme_buttons):
            if draw_button(theme, theme_start_x + i * (button_width + button_spacing), y_position, button_width, button_height, WHITE, GRAY, lambda t=theme: {"theme": t}):
                settings.update({"theme": theme})
        
        # Start Game button
        y_position += button_height + button_spacing
        if draw_button("Start Game", width // 2 - button_width // 2, y_position, button_width, button_height, WHITE, GRAY, lambda: True):
            return settings
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pygame.display.update()
        clock.tick(15)

def show_score(score, color):
    score_text = small_font.render(f"Score: {score}", True, color)
    window.blit(score_text, [10, 10])

def gameLoop(settings):
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    # Super block properties
    super_block_active = False
    super_block_timer = 0
    super_block_duration = 100  # Duration in game ticks

    score = 0

    while not game_over:

        while game_close:
            window.fill(THEMES[settings["theme"]]["background"])
            message("You Lost!", THEMES[settings["theme"]]["text"], -50)
            message(f"Final Score: {score}", THEMES[settings["theme"]]["text"], 0)
            message("Press Q-Quit or C-Play Again", THEMES[settings["theme"]]["text"], 50, "small")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        settings = game_settings()
                        gameLoop(settings)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Implement wraparound movement
        x1 += x1_change
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block

        y1 += y1_change
        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - snake_block

        window.fill(THEMES[settings["theme"]]["background"])
        if settings["show_grid"]:
            draw_grid()

        # Draw food or super block
        if super_block_active:
            pygame.draw.rect(window, GOLD, [foodx, foody, snake_block, snake_block])
            super_block_timer += 1
            if super_block_timer >= super_block_duration:
                super_block_active = False
                super_block_timer = 0
        else:
            pygame.draw.rect(window, THEMES[settings["theme"]]["food"], [foodx, foody, snake_block, snake_block])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list, THEMES[settings["theme"]]["snake"])
        show_score(score, THEMES[settings["theme"]]["text"])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            if super_block_active:
                length_of_snake += 10  # Increase length by 10 for super block
                score += 100  # 10 times the normal score
                super_block_active = False
                super_block_timer = 0
            else:
                length_of_snake += 1
                score += 10
                if random.random() < 0.2:  # 20% chance of spawning a super block
                    super_block_active = True

        clock.tick(settings["speed"])

    pygame.quit()
    quit()

settings = game_settings()
gameLoop(settings)