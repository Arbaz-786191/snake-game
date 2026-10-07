import pygame
import random
import sys
import math

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


# =========================================================
# BOUNDARY
# =========================================================

BOUNDARY_LEFT = 20
BOUNDARY_TOP = 60
BOUNDARY_RIGHT = 780
BOUNDARY_BOTTOM = 580


# =========================================================
# COLORS
# =========================================================

BLACK = (5, 8, 5)

GRASS_DARK = (10, 28, 12)
GRASS = (18, 48, 20)
GRASS_LIGHT = (35, 75, 30)

GREEN = (55, 185, 55)
LIGHT_GREEN = (105, 225, 90)
DARK_GREEN = (20, 85, 28)
VERY_DARK_GREEN = (8, 40, 14)

WHITE = (245, 245, 245)
GRAY = (150, 155, 145)
DARK_GRAY = (55, 60, 55)

YELLOW = (255, 215, 60)

RED = (210, 40, 35)
LIGHT_RED = (255, 100, 80)
DARK_RED = (105, 15, 15)

BROWN = (105, 60, 25)
DARK_BROWN = (55, 30, 12)
WOOD = (125, 72, 30)

STONE_DARK = (38, 42, 36)
STONE = (82, 87, 77)
STONE_LIGHT = (125, 130, 112)

BANANA = (245, 205, 45)
BANANA_LIGHT = (255, 230, 90)

GRAPE = (105, 45, 165)
GRAPE_LIGHT = (150, 80, 205)

ORANGE = (245, 125, 20)
ORANGE_LIGHT = (255, 180, 55)

LEAF_GREEN = (45, 135, 45)


# =========================================================
# FONTS
# =========================================================

title_font = pygame.font.Font(None, 88)
menu_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 30)
score_font = pygame.font.Font(None, 32)
game_over_font = pygame.font.Font(None, 76)


# =========================================================
# FRUIT SEQUENCE
# =========================================================

FRUITS = [
    "APPLE",
    "BANANA",
    "GRAPES",
    "ORANGE"
]


# =========================================================
# RANDOM GRASS DETAILS
# =========================================================

grass_details = []

random.seed(7)

for _ in range(180):

    x = random.randint(
        BOUNDARY_LEFT + 10,
        BOUNDARY_RIGHT - 10
    )

    y = random.randint(
        BOUNDARY_TOP + 10,
        BOUNDARY_BOTTOM - 10
    )

    size = random.randint(1, 3)

    grass_details.append(
        (x, y, size)
    )


# =========================================================
# CREATE FOOD
# =========================================================

def create_food(snake):

    while True:

        food = [
            random.randrange(
                BOUNDARY_LEFT + CELL_SIZE,
                BOUNDARY_RIGHT - CELL_SIZE,
                CELL_SIZE
            ),
            random.randrange(
                BOUNDARY_TOP + CELL_SIZE,
                BOUNDARY_BOTTOM - CELL_SIZE,
                CELL_SIZE
            )
        ]

        if food not in snake:
            return food


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    snake = [
        [400, 300],
        [380, 300],
        [360, 300]
    ]

    direction = "RIGHT"

    food = create_food(snake)

    fruit_index = 0

    score = 0

    return snake, direction, food, fruit_index, score


# =========================================================
# TEXT WITH SHADOW
# =========================================================

def draw_text_shadow(
    text,
    font,
    color,
    position,
    shadow_color=(0, 0, 0),
    shadow_offset=3
):

    shadow = font.render(
        text,
        True,
        shadow_color
    )

    screen.blit(
        shadow,
        (
            position[0] + shadow_offset,
            position[1] + shadow_offset
        )
    )

    main = font.render(
        text,
        True,
        color
    )

    screen.blit(
        main,
        position
    )


# =========================================================
# BACKGROUND
# =========================================================

def draw_background():

    screen.fill(GRASS_DARK)

    # Grass bands

    for y in range(
        BOUNDARY_TOP,
        BOUNDARY_BOTTOM,
        4
    ):

        shade = 10 + int(
            7 * math.sin(y * 0.03)
        )

        pygame.draw.line(
            screen,
            (
                10,
                28 + shade,
                12
            ),
            (
                BOUNDARY_LEFT,
                y
            ),
            (
                BOUNDARY_RIGHT,
                y
            )
        )


    # Subtle grid

    for x in range(
        BOUNDARY_LEFT,
        BOUNDARY_RIGHT,
        CELL_SIZE
    ):

        pygame.draw.line(
            screen,
            (17, 43, 19),
            (x, BOUNDARY_TOP),
            (x, BOUNDARY_BOTTOM),
            1
        )


    for y in range(
        BOUNDARY_TOP,
        BOUNDARY_BOTTOM,
        CELL_SIZE
    ):

        pygame.draw.line(
            screen,
            (17, 43, 19),
            (BOUNDARY_LEFT, y),
            (BOUNDARY_RIGHT, y),
            1
        )


    # Small grass details

    for x, y, size in grass_details:

        pygame.draw.line(
            screen,
            GRASS_LIGHT,
            (x, y + 5),
            (x - 2, y),
            size
        )

        pygame.draw.line(
            screen,
            GRASS_LIGHT,
            (x, y + 5),
            (x + 2, y),
            size
        )


# =========================================================
# STONE BLOCK
# =========================================================

def draw_stone_block(rect):

    x, y, w, h = rect

    pygame.draw.rect(
        screen,
        (25, 28, 24),
        (x + 2, y + 3, w, h),
        border_radius=5
    )

    pygame.draw.rect(
        screen,
        STONE,
        (x, y, w, h),
        border_radius=5
    )

    pygame.draw.line(
        screen,
        STONE_LIGHT,
        (x + 4, y + 3),
        (x + w - 5, y + 3),
        2
    )

    pygame.draw.line(
        screen,
        STONE_DARK,
        (x + 4, y + h - 3),
        (x + w - 5, y + h - 3),
        2
    )


# =========================================================
# BOUNDARY
# =========================================================

def draw_boundary():

    # Dark outer frame

    pygame.draw.rect(
        screen,
        (22, 25, 21),
        (
            BOUNDARY_LEFT - 3,
            BOUNDARY_TOP - 3,
            BOUNDARY_RIGHT - BOUNDARY_LEFT + 6,
            BOUNDARY_BOTTOM - BOUNDARY_TOP + 6
        ),
        border_radius=8
    )


    # Top stones

    stone_w = 38

    x = BOUNDARY_LEFT

    while x < BOUNDARY_RIGHT:

        width = min(
            stone_w,
            BOUNDARY_RIGHT - x
        )

        draw_stone_block(
            (
                x,
                BOUNDARY_TOP - 1,
                width - 2,
                18
            )
        )

        x += stone_w


    # Bottom stones

    x = BOUNDARY_LEFT

    while x < BOUNDARY_RIGHT:

        width = min(
            stone_w,
            BOUNDARY_RIGHT - x
        )

        draw_stone_block(
            (
                x,
                BOUNDARY_BOTTOM - 17,
                width - 2,
                18
            )
        )

        x += stone_w


    # Left stones

    y = BOUNDARY_TOP + 17

    while y < BOUNDARY_BOTTOM - 17:

        height = min(
            34,
            BOUNDARY_BOTTOM - 17 - y
        )

        draw_stone_block(
            (
                BOUNDARY_LEFT - 1,
                y,
                18,
                height - 2
            )
        )

        y += 34


    # Right stones

    y = BOUNDARY_TOP + 17

    while y < BOUNDARY_BOTTOM - 17:

        height = min(
            34,
            BOUNDARY_BOTTOM - 17 - y
        )

        draw_stone_block(
            (
                BOUNDARY_RIGHT - 17,
                y,
                18,
                height - 2
            )
        )

        y += 34


# =========================================================
# FRUIT GLOW
# =========================================================

def draw_fruit_glow(x, y, color, animation_time):

    pulse = int(
        3 + math.sin(animation_time * 5) * 2
    )

    glow_surface = pygame.Surface(
        (50, 50),
        pygame.SRCALPHA
    )

    pygame.draw.circle(
        glow_surface,
        (*color, 35),
        (25, 25),
        15 + pulse
    )

    screen.blit(
        glow_surface,
        (x - 25, y - 25)
    )


# =========================================================
# APPLE
# =========================================================

def draw_apple(x, y):

    # Shadow

    pygame.draw.ellipse(
        screen,
        (5, 15, 5),
        (x - 10, y + 7, 20, 7)
    )

    # Apple body

    pygame.draw.circle(
        screen,
        DARK_RED,
        (x - 5, y),
        10
    )

    pygame.draw.circle(
        screen,
        DARK_RED,
        (x + 5, y),
        10
    )

    pygame.draw.circle(
        screen,
        RED,
        (x - 4, y - 2),
        9
    )

    pygame.draw.circle(
        screen,
        RED,
        (x + 4, y - 2),
        9
    )

    # Highlight

    pygame.draw.ellipse(
        screen,
        LIGHT_RED,
        (x - 7, y - 7, 5, 7)
    )

    # Stem

    pygame.draw.line(
        screen,
        DARK_BROWN,
        (x, y - 8),
        (x + 2, y - 15),
        3
    )

    # Leaf

    pygame.draw.ellipse(
        screen,
        LEAF_GREEN,
        (x + 1, y - 16, 11, 6)
    )


# =========================================================
# BANANA
# =========================================================

def draw_banana(x, y):

    # Shadow

    pygame.draw.ellipse(
        screen,
        (5, 15, 5),
        (x - 11, y + 6, 24, 7)
    )

    points = [
        (x - 9, y - 7),
        (x - 4, y - 11),
        (x + 9, y - 4),
        (x + 11, y + 2),
        (x + 7, y + 8),
        (x + 1, y + 9),
        (x + 4, y + 3),
        (x - 2, y),
        (x - 7, y - 1)
    ]

    pygame.draw.polygon(
        screen,
        BANANA,
        points
    )

    # Highlight

    pygame.draw.line(
        screen,
        BANANA_LIGHT,
        (x - 4, y - 5),
        (x + 7, y + 2),
        3
    )

    # Ends

    pygame.draw.circle(
        screen,
        DARK_BROWN,
        (x - 8, y - 7),
        2
    )

    pygame.draw.circle(
        screen,
        DARK_BROWN,
        (x + 9, y + 3),
        2
    )


# =========================================================
# GRAPES
# =========================================================

def draw_grapes(x, y):

    grape_positions = [
        (-5, -8),
        (5, -8),

        (-9, 0),
        (0, 0),
        (9, 0),

        (-6, 8),
        (5, 8),

        (0, 15)
    ]

    # Shadow

    pygame.draw.ellipse(
        screen,
        (5, 15, 5),
        (x - 12, y + 15, 25, 7)
    )

    for gx, gy in grape_positions:

        pygame.draw.circle(
            screen,
            (55, 20, 85),
            (x + gx, y + gy + 2),
            6
        )

        pygame.draw.circle(
            screen,
            GRAPE,
            (x + gx, y + gy),
            5
        )

        pygame.draw.circle(
            screen,
            GRAPE_LIGHT,
            (x + gx - 2, y + gy - 2),
            2
        )

    # Stem

    pygame.draw.line(
        screen,
        DARK_BROWN,
        (x, y - 11),
        (x + 2, y - 17),
        3
    )

    # Leaf

    pygame.draw.ellipse(
        screen,
        LEAF_GREEN,
        (x - 8, y - 18, 13, 7)
    )


# =========================================================
# ORANGE
# =========================================================

def draw_orange(x, y):

    # Shadow

    pygame.draw.ellipse(
        screen,
        (5, 15, 5),
        (x - 11, y + 7, 22, 7)
    )

    # Dark outside

    pygame.draw.circle(
        screen,
        (160, 65, 5),
        (x, y + 1),
        11
    )

    # Orange body

    pygame.draw.circle(
        screen,
        ORANGE,
        (x, y),
        9
    )

    # Highlight

    pygame.draw.ellipse(
        screen,
        ORANGE_LIGHT,
        (x - 6, y - 6, 5, 6)
    )

    # Small texture

    for angle in range(0, 360, 45):

        rad = math.radians(angle)

        px = int(
            x + math.cos(rad) * 6
        )

        py = int(
            y + math.sin(rad) * 6
        )

        pygame.draw.circle(
            screen,
            (225, 105, 10),
            (px, py),
            1
        )

    # Leaf

    pygame.draw.ellipse(
        screen,
        LEAF_GREEN,
        (x + 1, y - 13, 10, 6)
    )


# =========================================================
# DRAW FRUIT
# =========================================================

def draw_fruit(food, fruit_type, animation_time):

    x, y = food

    if fruit_type == "APPLE":

        glow_color = (255, 60, 40)

    elif fruit_type == "BANANA":

        glow_color = (255, 220, 60)

    elif fruit_type == "GRAPES":

        glow_color = (150, 70, 220)

    else:

        glow_color = (255, 150, 30)


    draw_fruit_glow(
        x,
        y,
        glow_color,
        animation_time
    )


    if fruit_type == "APPLE":

        draw_apple(x, y)

    elif fruit_type == "BANANA":

        draw_banana(x, y)

    elif fruit_type == "GRAPES":

        draw_grapes(x, y)

    elif fruit_type == "ORANGE":

        draw_orange(x, y)


# =========================================================
# SNAKE BODY
# =========================================================

def draw_snake(snake, direction):

    # Connected body

    for i in range(len(snake) - 1):

        x1, y1 = snake[i]
        x2, y2 = snake[i + 1]

        pygame.draw.line(
            screen,
            VERY_DARK_GREEN,
            (x1, y1 + 2),
            (x2, y2 + 2),
            21
        )

        pygame.draw.line(
            screen,
            DARK_GREEN,
            (x1, y1),
            (x2, y2),
            18
        )


    # Body segments

    for i in range(
        len(snake) - 1,
        0,
        -1
    ):

        x, y = snake[i]

        # Shadow

        pygame.draw.circle(
            screen,
            (5, 30, 8),
            (x, y + 3),
            11
        )

        # Body

        pygame.draw.circle(
            screen,
            DARK_GREEN,
            (x, y),
            10
        )

        pygame.draw.circle(
            screen,
            GREEN,
            (x, y - 1),
            8
        )

        # Shine

        pygame.draw.circle(
            screen,
            LIGHT_GREEN,
            (x - 3, y - 4),
            2
        )


    # =====================================================
    # HEAD
    # =====================================================

    head_x, head_y = snake[0]

    # Shadow

    pygame.draw.circle(
        screen,
        (4, 30, 8),
        (head_x, head_y + 4),
        14
    )

    # Outer head

    pygame.draw.circle(
        screen,
        DARK_GREEN,
        (head_x, head_y),
        13
    )

    # Main head

    pygame.draw.circle(
        screen,
        GREEN,
        (head_x, head_y - 1),
        11
    )

    # Head shine

    pygame.draw.circle(
        screen,
        LIGHT_GREEN,
        (head_x - 4, head_y - 5),
        3
    )


    # =====================================================
    # EYES
    # =====================================================

    if direction == "RIGHT":

        eyes = [
            (head_x + 5, head_y - 5),
            (head_x + 5, head_y + 5)
        ]

    elif direction == "LEFT":

        eyes = [
            (head_x - 5, head_y - 5),
            (head_x - 5, head_y + 5)
        ]

    elif direction == "UP":

        eyes = [
            (head_x - 5, head_y - 5),
            (head_x + 5, head_y - 5)
        ]

    else:

        eyes = [
            (head_x - 5, head_y + 5),
            (head_x + 5, head_y + 5)
        ]


    for ex, ey in eyes:

        pygame.draw.circle(
            screen,
            WHITE,
            (ex, ey),
            3
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (ex, ey),
            1
        )


    # =====================================================
    # TONGUE
    # =====================================================

    tongue = (235, 55, 75)

    if direction == "RIGHT":

        start = (head_x + 10, head_y)
        end = (head_x + 18, head_y)

        pygame.draw.line(
            screen,
            tongue,
            start,
            end,
            2
        )

        pygame.draw.line(
            screen,
            tongue,
            end,
            (head_x + 22, head_y - 3),
            2
        )

        pygame.draw.line(
            screen,
            tongue,
            end,
            (head_x + 22, head_y + 3),
            2
        )

    elif direction == "LEFT":

        start = (head_x - 10, head_y)
        end = (head_x - 18, head_y)

        pygame.draw.line(
            screen,
            tongue,
            start,
            end,
            2
        )

        pygame.draw.line(
            screen,
            tongue,
            end,
            (head_x - 22, head_y - 3),
            2
        )

        pygame.draw.line(
            screen,
            tongue,
            end,
            (head_x - 22, head_y + 3),
            2
        )

    elif direction == "UP":

        start = (head_x, head_y - 10)
        end = (head_x, head_y - 18)

        pygame.draw.line(
            screen,
            tongue,
            start,
            end,
            2
        )

        pygame.draw.line(
            screen,
            tongue,
            end,
            (head_x - 3, head_y - 22),
            2
        )

        pygame.draw.line(
            screen,
            tongue,
            end,
            (head_x + 3, head_y - 22),
            2
        )

    else:

        start = (head_x, head_y + 10)
        end = (head_x, head_y + 18)

        pygame.draw.line(
            screen,
            tongue,
            start,
            end,
            2
        )

        pygame.draw.line(
            screen,
            tongue,
            end,
            (head_x - 3, head_y + 22),
            2
        )

        pygame.draw.line(
            screen,
            tongue,
            end,
            (head_x + 3, head_y + 22),
            2
        )


# =========================================================
# PARTICLES
# =========================================================

def create_eating_particles(food):

    particles = []

    for _ in range(18):

        particles.append({
            "x": food[0],
            "y": food[1],
            "vx": random.uniform(-2.5, 2.5),
            "vy": random.uniform(-2.5, 2.5),
            "life": random.randint(15, 30)
        })

    return particles


def update_particles(particles):

    for particle in particles:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["life"] -= 1


def draw_particles(particles):

    for particle in particles:

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            2
        )


# =========================================================
# MENU PANEL
# =========================================================

def draw_menu_panel():

    panel = pygame.Surface(
        (390, 300),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        panel,
        (5, 15, 8, 225),
        (0, 0, 390, 300),
        border_radius=18
    )

    pygame.draw.rect(
        panel,
        (90, 130, 85, 100),
        (1, 1, 388, 298),
        2,
        border_radius=18
    )

    screen.blit(
        panel,
        (
            WIDTH // 2 - 195,
            190
        )
    )


# =========================================================
# MENU BUTTON
# =========================================================

def draw_menu_button(
    text,
    y,
    selected=False
):

    x = WIDTH // 2 - 135
    w = 270
    h = 48

    if selected:

        pygame.draw.rect(
            screen,
            (12, 75, 25),
            (x + 2, y + 3, w, h),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (50, 175, 55),
            (x, y, w, h),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (125, 235, 105),
            (x + 2, y + 2, w - 4, 2),
            border_radius=2
        )

        color = YELLOW

    else:

        pygame.draw.rect(
            screen,
            (20, 35, 20),
            (x + 2, y + 3, w, h),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (55, 75, 52),
            (x, y, w, h),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (100, 120, 95),
            (x, y, w, h),
            1,
            border_radius=10
        )

        color = WHITE


    text_surface = menu_font.render(
        text,
        True,
        color
    )

    screen.blit(
        text_surface,
        (
            WIDTH // 2 - text_surface.get_width() // 2,
            y + 5
        )
    )


# =========================================================
# START MENU
# =========================================================

def show_start_menu():

    selected = 0

    options = [
        ("EASY", 8),
        ("MEDIUM", 12),
        ("HARD", 17)
    ]

    animation = 0


    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:

                    selected -= 1

                    if selected < 0:
                        selected = 2


                elif event.key == pygame.K_DOWN:

                    selected += 1

                    if selected > 2:
                        selected = 0


                elif event.key == pygame.K_RETURN:

                    return options[selected][1]


                elif event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()


        animation += 0.04


        # Background

        screen.fill(
            (7, 15, 8)
        )


        # Fake forest background

        for y in range(
            0,
            HEIGHT,
            8
        ):

            shade = int(
                8 * math.sin(
                    y * 0.03
                )
            )

            pygame.draw.line(
                screen,
                (
                    5,
                    18 + shade,
                    7
                ),
                (0, y),
                (WIDTH, y)
            )


        # Decorative grass

        for x in range(
            0,
            WIDTH,
            18
        ):

            pygame.draw.line(
                screen,
                GRASS,
                (x, HEIGHT),
                (x + 5, HEIGHT - 30),
                2
            )


        # Title shadow

        title_shadow = title_font.render(
            "SNAKE GAME",
            True,
            (0, 0, 0)
        )

        screen.blit(
            title_shadow,
            (
                WIDTH // 2
                - title_shadow.get_width() // 2
                + 5,
                82
            )
        )


        # Title

        title = title_font.render(
            "SNAKE GAME",
            True,
            GREEN
        )

        screen.blit(
            title,
            (
                WIDTH // 2
                - title.get_width() // 2,
                77
            )
        )


        # Title highlight

        highlight = title_font.render(
            "SNAKE GAME",
            True,
            LIGHT_GREEN
        )

        screen.blit(
            highlight,
            (
                WIDTH // 2
                - highlight.get_width() // 2,
                74
            )
        )


        # Menu panel

        draw_menu_panel()


        subtitle = small_font.render(
            "CHOOSE DIFFICULTY",
            True,
            GRAY
        )

        screen.blit(
            subtitle,
            (
                WIDTH // 2
                - subtitle.get_width() // 2,
                210
            )
        )


        # Difficulty buttons

        for i, (name, speed) in enumerate(options):

            draw_menu_button(
                name,
                250 + i * 55,
                i == selected
            )


        # Controls

        controls = small_font.render(
            "↑  ↓   SELECT       ENTER   CONFIRM",
            True,
            GRAY
        )

        screen.blit(
            controls,
            (
                WIDTH // 2
                - controls.get_width() // 2,
                470
            )
        )


        pygame.display.flip()

        clock.tick(60)


# =========================================================
# GAME
# =========================================================

def play_game(speed):

    snake, direction, food, fruit_index, score = reset_game()

    next_direction = direction

    game_over = False

    particles = []

    animation_time = 0

    game_over_timer = 0


    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:

                    if direction != "DOWN":
                        next_direction = "UP"


                elif event.key == pygame.K_DOWN:

                    if direction != "UP":
                        next_direction = "DOWN"


                elif event.key == pygame.K_LEFT:

                    if direction != "RIGHT":
                        next_direction = "LEFT"


                elif event.key == pygame.K_RIGHT:

                    if direction != "LEFT":
                        next_direction = "RIGHT"


                elif event.key == pygame.K_r:

                    if game_over:

                        snake, direction, food, fruit_index, score = reset_game()

                        next_direction = direction

                        game_over = False

                        particles = []

                        game_over_timer = 0


                elif event.key == pygame.K_ESCAPE:

                    return


        # =================================================
        # MOVEMENT
        # =================================================

        if not game_over:

            direction = next_direction

            head_x = snake[0][0]
            head_y = snake[0][1]


            if direction == "UP":

                head_y -= CELL_SIZE

            elif direction == "DOWN":

                head_y += CELL_SIZE

            elif direction == "LEFT":

                head_x -= CELL_SIZE

            elif direction == "RIGHT":

                head_x += CELL_SIZE


            new_head = [
                head_x,
                head_y
            ]


            # Boundary collision

            if (
                head_x < BOUNDARY_LEFT + CELL_SIZE
                or head_x >= BOUNDARY_RIGHT - CELL_SIZE
                or head_y < BOUNDARY_TOP + CELL_SIZE
                or head_y >= BOUNDARY_BOTTOM - CELL_SIZE
            ):

                game_over = True


            # Self collision

            if new_head in snake:

                game_over = True


            if not game_over:

                snake.insert(
                    0,
                    new_head
                )


                # =================================================
                # EAT FRUIT
                # =================================================

                if new_head == food:

                    score += 1

                    particles = create_eating_particles(
                        food
                    )


                    # Next fruit

                    fruit_index += 1

                    if fruit_index >= len(FRUITS):

                        fruit_index = 0


                    food = create_food(
                        snake
                    )

                else:

                    snake.pop()


        # =================================================
        # PARTICLES
        # =================================================

        update_particles(
            particles
        )

        particles = [
            p for p in particles
            if p["life"] > 0
        ]


        # =================================================
        # ANIMATION
        # =================================================

        animation_time += 0.05


        if game_over:

            game_over_timer += 1


        # =================================================
        # DRAW GAME
        # =================================================

        draw_background()

        draw_boundary()

        draw_fruit(
            food,
            FRUITS[fruit_index],
            animation_time
        )

        draw_snake(
            snake,
            direction
        )

        draw_particles(
            particles
        )


        # =================================================
        # SCORE PANEL
        # =================================================

        pygame.draw.rect(
            screen,
            (35, 25, 12),
            (25, 12, 145, 38),
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            (120, 75, 25),
            (25, 12, 145, 38),
            2,
            border_radius=8
        )

        score_text = score_font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (38, 18)
        )


        # =================================================
        # DIFFICULTY PANEL
        # =================================================

        if speed == 8:

            difficulty_name = "EASY"

        elif speed == 12:

            difficulty_name = "MEDIUM"

        else:

            difficulty_name = "HARD"


        difficulty_text = score_font.render(
            difficulty_name,
            True,
            YELLOW
        )


        panel_width = (
            difficulty_text.get_width()
            + 35
        )


        pygame.draw.rect(
            screen,
            (35, 25, 12),
            (
                WIDTH - panel_width - 25,
                12,
                panel_width,
                38
            ),
            border_radius=8
        )


        pygame.draw.rect(
            screen,
            (120, 75, 25),
            (
                WIDTH - panel_width - 25,
                12,
                panel_width,
                38
            ),
            2,
            border_radius=8
        )


        screen.blit(
            difficulty_text,
            (
                WIDTH
                - panel_width
                - 8,
                18
            )
        )


        # =================================================
        # GAME OVER
        # =================================================

        if game_over:

            alpha = min(
                190,
                game_over_timer * 5
            )


            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, alpha)
            )

            screen.blit(
                overlay,
                (0, 0)
            )


            # Game over panel

            panel_w = 430
            panel_h = 260

            panel_x = (
                WIDTH // 2
                - panel_w // 2
            )

            panel_y = 160


            pygame.draw.rect(
                screen,
                (15, 20, 15),
                (
                    panel_x + 4,
                    panel_y + 5,
                    panel_w,
                    panel_h
                ),
                border_radius=20
            )


            pygame.draw.rect(
                screen,
                (45, 60, 42),
                (
                    panel_x,
                    panel_y,
                    panel_w,
                    panel_h
                ),
                border_radius=20
            )


            pygame.draw.rect(
                screen,
                (105, 130, 95),
                (
                    panel_x,
                    panel_y,
                    panel_w,
                    panel_h
                ),
                2,
                border_radius=20
            )


            game_over_text = game_over_font.render(
                "GAME OVER",
                True,
                (235, 65, 45)
            )


            screen.blit(
                game_over_text,
                (
                    WIDTH // 2
                    - game_over_text.get_width() // 2,
                    185
                )
            )


            final_score = score_font.render(
                f"Final Score: {score}",
                True,
                WHITE
            )


            screen.blit(
                final_score,
                (
                    WIDTH // 2
                    - final_score.get_width() // 2,
                    270
                )
            )


            restart_text = small_font.render(
                "Press R to Restart",
                True,
                YELLOW
            )


            screen.blit(
                restart_text,
                (
                    WIDTH // 2
                    - restart_text.get_width() // 2,
                    325
                )
            )


            menu_text = small_font.render(
                "Press ESC for Menu",
                True,
                GRAY
            )


            screen.blit(
                menu_text,
                (
                    WIDTH // 2
                    - menu_text.get_width() // 2,
                    365
                )
            )


        pygame.display.flip()

        clock.tick(speed)


# =========================================================
# MAIN
# =========================================================

while True:

    speed = show_start_menu()

    play_game(speed)