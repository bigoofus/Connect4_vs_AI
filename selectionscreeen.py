import pygame
import sys
import gui as gui
import threading

def startscreen():
    # Initialize pygame
    pygame.init()

    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    LIGHT_GRAY = (230, 230, 230)
    DARK_GRAY = (180, 180, 180)
    FONT = pygame.font.SysFont("texgyreadventor-bold", 40)
    SMALL_FONT = pygame.font.SysFont("texgyreadventor-bold", 30)

    # Setup screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Connect 4 done by 8150-8197-8138")

    # Load background
    background = pygame.image.load("images/background.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load logo
    logo = pygame.image.load("images/Connect_4_game_logo.png")
    logo_width = 636
    logo_height = 201
    logo = pygame.transform.scale(logo, (logo_width, logo_height))

    # Input box
    input_width, input_height = 60, 40
    input_box = pygame.Rect((SCREEN_WIDTH - input_width) // 2 + 100, 200, input_width, input_height)
    search_depth = "3"
    input_active = False

    # Checkbox
    checkbox_size = 20
    checkbox_rect = pygame.Rect((SCREEN_WIDTH - checkbox_size) // 2 - 100, 250, checkbox_size, checkbox_size)
    show_tree_visualizer = False

    # Buttons
    button_texts = ["Minimax with Pruning", "Minimax without Pruning", "Expectiminimax"]
    buttons = []
    button_width = 450
    button_height = 50
    button_spacing = 20
    br = 12
    start_y = 340

    for i, text in enumerate(button_texts):
        rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + i * (button_height + button_spacing),
            button_width,
            button_height
        )
        buttons.append((text, rect))

    selected_mode = None

    # Main menu loop
    running = True
    while running:
        screen.blit(background, (0, 0))

        # Draw logo
        logo_x = (SCREEN_WIDTH - logo_width) // 2
        logo_y = 20
        screen.blit(logo, (logo_x, logo_y))

        # Title and input box
        title = FONT.render("Search Depth:", True, BLACK)
        title_rect = title.get_rect()
        title_rect.midright = (input_box.x - 10, input_box.y + input_height // 2)
        screen.blit(title, title_rect)

        pygame.draw.rect(screen, WHITE if input_active else GRAY, input_box, border_radius=12)
        text_surface = FONT.render(search_depth, True, BLACK)
        text_rect = text_surface.get_rect(center=input_box.center)
        screen.blit(text_surface, text_rect)

        # Checkbox and label
        pygame.draw.rect(screen, WHITE, checkbox_rect, border_radius=br)
        if show_tree_visualizer:
            pygame.draw.line(screen, BLACK, (checkbox_rect.x, checkbox_rect.y), (checkbox_rect.x + checkbox_size, checkbox_rect.y + checkbox_size), 3)
            pygame.draw.line(screen, BLACK, (checkbox_rect.x + checkbox_size, checkbox_rect.y), (checkbox_rect.x, checkbox_rect.y + checkbox_size), 3)

        checkbox_label = SMALL_FONT.render("Show Tree Visualizer", True, BLACK)
        checkbox_label_rect = checkbox_label.get_rect()
        checkbox_label_rect.midleft = (checkbox_rect.x + checkbox_size + 10, checkbox_rect.y + checkbox_size // 2)
        screen.blit(checkbox_label, checkbox_label_rect)

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for text, rect in buttons:
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, WHITE, rect, border_radius=br)
            else:
                pygame.draw.rect(screen, WHITE, rect, border_radius=br)

            label = SMALL_FONT.render(text, True, BLACK)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

                if checkbox_rect.collidepoint(event.pos):
                    show_tree_visualizer = not show_tree_visualizer

                for mode, rect in buttons:
                    if rect.collidepoint(event.pos):
                        selected_mode = mode
                        running = False

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    search_depth = search_depth[:-1]
                elif event.unicode.isdigit():
                    if event.unicode != "0":  # disallow "0"
                        search_depth = event.unicode  # replace instead of append

        pygame.display.update()

    # After menu
    if search_depth == "" or search_depth == "0":
        search_depth = 1
    else:
        search_depth = int(search_depth)
        search_depth = max(1, min(search_depth, 9))  # clamp to [1, 9]

    print(f"Selected Mode: {selected_mode}")
    print(f"Search Depth: {search_depth}")
    print(f"Show Tree Visualizer: {show_tree_visualizer}")
    
    gui.start_game(selected_mode, search_depth, show_tree_visualizer)
