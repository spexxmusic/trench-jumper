import pygame
import random

pygame.init()
if not pygame.get_init():
    print("Error: Pygame failed to initialize")
    input("Press Enter to exit...")
    exit()
print("Pygame initialized successfully")

BASE_WIDTH = 400
BASE_HEIGHT = 600
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
pygame.display.set_caption("Trench Jumper")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)

# Load background image
print("Attempting to load background image...")
try:
    background_image = pygame.image.load("bg.jpg").convert()
    background_image = pygame.transform.scale(background_image, (BASE_WIDTH, BASE_HEIGHT))
    print("Background image loaded successfully")
except FileNotFoundError:
    print("Background image not found, using white background")
    background_image = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
    background_image.fill(WHITE)
except Exception as e:
    print(f"Error loading background image: {e}")
    background_image = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
    background_image.fill(WHITE)

class Player:
    def __init__(self, start_y):
        try:
            self.base_image = pygame.image.load("sol.png").convert_alpha()
            self.width = 40
            self.height = 40
            self.image = pygame.transform.scale(self.base_image, (self.width, self.height))
            self.x = BASE_WIDTH // 2 - self.width // 2
            self.y = start_y - self.height
            self.velocity_y = 0
            self.jump_power = -15
            self.gravity = 0.5
            print("Player initialized successfully")
        except Exception as e:
            print(f"Error initializing player: {e}")
            raise

    def resize(self, screen_width, screen_height):
        scale_x = screen_width / BASE_WIDTH
        scale_y = screen_height / BASE_HEIGHT
        self.width = int(40 * scale_x)
        self.height = int(40 * scale_y)
        self.image = pygame.transform.scale(self.base_image, (self.width, self.height))
        self.x = screen_width // 2 - self.width // 2
        self.jump_power = -15 * scale_y
        self.gravity = 0.5 * scale_y

class Platform:
    def __init__(self, y):
        self.width = 80
        self.height = 20
        self.x = random.randint(0, BASE_WIDTH - self.width)
        self.y = y

    def resize(self, screen_width, screen_height):
        scale_x = screen_width / BASE_WIDTH
        scale_y = screen_height / BASE_HEIGHT
        self.width = int(80 * scale_x)
        self.height = int(20 * scale_y)
        self.x = int(self.x * scale_x)
        self.y = int(self.y * scale_y)

class Floor:
    def __init__(self):
        self.width = BASE_WIDTH
        self.height = 50
        self.x = 0
        self.y = BASE_HEIGHT - self.height

    def resize(self, screen_width, screen_height):
        scale_x = screen_width / BASE_WIDTH
        scale_y = screen_height / BASE_HEIGHT
        self.width = int(BASE_WIDTH * scale_x)
        self.height = int(50 * scale_y)
        self.x = 0
        self.y = screen_height - self.height

# Leaderboard storage
leaderboard = []

def start_screen():
    font = pygame.font.Font(None, 60)  # Bigger font size (60)
    # Render black outline text slightly offset
    title_outline = font.render("Trench Jumper", True, BLACK)
    title = font.render("Trench Jumper", True, BLUE)  # Blue text
    input_box = pygame.Rect(BASE_WIDTH // 2 - 100, BASE_HEIGHT // 2 - 20, 200, 40)
    start_button = pygame.Rect(BASE_WIDTH // 2 - 50, BASE_HEIGHT // 2 + 50, 100, 40)
    color_inactive = GRAY
    color_active = WHITE
    color = color_inactive
    active = False
    name = ""
    
    print("Entered start screen...")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                    color = color_active if active else color_inactive
                if start_button.collidepoint(event.pos) and name:
                    print(f"Start clicked with name: {name}")
                    return name
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and name:
                        print(f"Enter pressed with name: {name}")
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name = name + event.unicode

        screen.blit(background_image, (0, 0))
        txt_surface = font.render(name, True, color)
        # Draw black outline slightly offset for thickness
        screen.blit(title_outline, (BASE_WIDTH // 2 - title_outline.get_width() // 2 - 2, BASE_HEIGHT // 2 - 100 - 2))
        screen.blit(title_outline, (BASE_WIDTH // 2 - title_outline.get_width() // 2 + 2, BASE_HEIGHT // 2 - 100 + 2))
        screen.blit(title_outline, (BASE_WIDTH // 2 - title_outline.get_width() // 2 - 2, BASE_HEIGHT // 2 - 100 + 2))
        screen.blit(title_outline, (BASE_WIDTH // 2 - title_outline.get_width() // 2 + 2, BASE_HEIGHT // 2 - 100 - 2))
        # Draw blue text on top
        screen.blit(title, (BASE_WIDTH // 2 - title.get_width() // 2, BASE_HEIGHT // 2 - 100))
        pygame.draw.rect(screen, color, input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, GRAY, start_button)
        start_text = font.render("Start", True, WHITE)
        screen.blit(start_text, (start_button.x + 15, start_button.y + 5))
        
        pygame.display.flip()
        clock.tick(60)

def leaderboard_screen(score, name):
    leaderboard.append((name, score))
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    leaderboard[:] = leaderboard[:5]
    
    font = pygame.font.Font(None, 36)
    print("Entered leaderboard screen...")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print("Exiting leaderboard screen...")
                return
        
        screen.blit(background_image, (0, 0))
        game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
        screen.blit(game_over_text, (BASE_WIDTH // 2 - game_over_text.get_width() // 2, BASE_HEIGHT // 4))
        
        for i, (n, s) in enumerate(leaderboard):
            entry = font.render(f"{i+1}. {n}: {s}", True, WHITE)
            screen.blit(entry, (BASE_WIDTH // 2 - entry.get_width() // 2, BASE_HEIGHT // 2 + i * 40))
        
        restart_text = font.render("Press Enter to Restart", True, WHITE)
        screen.blit(restart_text, (BASE_WIDTH // 2 - restart_text.get_width() // 2, BASE_HEIGHT - 50))
        
        pygame.display.flip()
        clock.tick(60)

def main_game(name):
    global screen
    try:
        floor = Floor()
        player = Player(BASE_HEIGHT - floor.height)
        platforms = [Platform(BASE_HEIGHT - 150)]
        scroll_speed = 2
        score = 0
        fullscreen = False
        background_image_scaled = background_image
        
        running = True
        print(f"Starting game with name: {name}")
        print(f"Player starting y: {player.y}, Floor y: {floor.y}, First platform y: {platforms[0].y}")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
                        screen_width, screen_height = screen.get_size()
                        background_image_scaled = pygame.transform.scale(background_image, (screen_width, screen_height))
                        player.resize(screen_width, screen_height)
                        floor.resize(screen_width, screen_height)
                        for platform in platforms:
                            platform.resize(screen_width, screen_height)

            keys = pygame.key.get_pressed()
            screen_width, screen_height = screen.get_size()
            if keys[pygame.K_LEFT] and player.x > 0:
                player.x -= 5 * (screen_width / BASE_WIDTH)
            if keys[pygame.K_RIGHT] and player.x < screen_width - player.width:
                player.x += 5 * (screen_width / BASE_WIDTH)

            player.velocity_y += player.gravity
            player.y += player.velocity_y

            if (player.y + player.height >= floor.y and
                player.velocity_y > 0):
                player.y = floor.y - player.height
                player.velocity_y = player.jump_power

            for platform in platforms[:]:
                if (player.y + player.height >= platform.y and
                    player.y + player.height <= platform.y + platform.height and
                    player.x + player.width > platform.x and
                    player.x < platform.x + platform.width and
                    player.velocity_y > 0):
                    player.y = platform.y - player.height
                    player.velocity_y = player.jump_power

            if player.y < screen_height // 2 and player.velocity_y < 0:
                scroll = -player.velocity_y
                player.y += scroll
                floor.y += scroll
                for platform in platforms:
                    platform.y += scroll
                score += int(scroll * (BASE_HEIGHT / screen_height))

            if platforms[-1].y > 100 * (screen_height / BASE_HEIGHT):
                platforms.append(Platform(platforms[-1].y - random.randint(80, 120) * (screen_height / BASE_HEIGHT)))

            platforms = [p for p in platforms if p.y < screen_height]

            if player.y > screen_height:
                running = False

            screen.blit(background_image_scaled, (0, 0))
            pygame.draw.rect(screen, WHITE, (floor.x, floor.y, floor.width, floor.height))
            screen.blit(player.image, (player.x, player.y))
            for platform in platforms:
                pygame.draw.rect(screen, WHITE, (platform.x, platform.y, platform.width, platform.height))
            
            font_size = int(36 * (screen_width / BASE_WIDTH))
            font = pygame.font.Font(None, font_size)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)
        
        leaderboard_screen(score, name)
    except Exception as e:
        print(f"Crash in main_game: {e}")
        input("Press Enter to see crash details...")

# Main loop
clock = pygame.time.Clock()
while True:
    name = start_screen()
    main_game(name)