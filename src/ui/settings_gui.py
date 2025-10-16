import pygame

WINDOW_WIDTH = 350
WINDOW_HEIGHT = 400
START_BUTTON_WIDTH = 130
START_BUTTON_HEIGHT = 40

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BACKGROUND_COLOR = (50, 50, 60)
BLUE = (0, 102, 204)
LIGHT_BLUE = (102, 178, 255)

BOARD_SIZES = ["6x6", "7x6", "8x7", "8x8"]
DIFFICULTY_OPTIONS = ["Easy", "Medium", "Hard"]

DEFAULT_SELECTION = 0


class RadioButton:
    def __init__(self, x, y, text, group):
        pygame.init()

        self.rectangle_area = pygame.Rect(x, y, 20, 20)
        self.text = text
        self.selected = False
        self.group = group
        group.append(self)

    def draw(self, screen):
        font = pygame.font.SysFont("Poppins-Regular.ttf", 26)

        pygame.draw.circle(screen, BLUE if self.selected else GRAY, self.rectangle_area.center, 10)
        if self.selected:
            pygame.draw.circle(screen, WHITE, self.rectangle_area.center, 5)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rectangle_area.right + 8, self.rectangle_area.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rectangle_area.collidepoint(event.pos):
            for button in self.group:
                button.selected = False
            self.selected = True

    def is_selected(self):
        return self.selected


class SettingsGUI:
    def __init__(self):

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Obstruction - Settings")

        self.running = True

        self.board_size_buttons = []
        for selected_index, size in enumerate(BOARD_SIZES):
            button = RadioButton(50, 50 + selected_index * 40, size, self.board_size_buttons)
            if selected_index == DEFAULT_SELECTION:
                button.selected = True

        self.difficulty_buttons = []
        for selected_index, difficulty in enumerate(DIFFICULTY_OPTIONS):
            button = RadioButton(200, 50 + selected_index * 40, difficulty, self.difficulty_buttons)
            if selected_index == DEFAULT_SELECTION:
                button.selected = True

        self.play_first_buttons = []
        self.play_first_text = "Do you want to play first?"
        RadioButton(90, 250, "Yes", self.play_first_buttons)
        RadioButton(180, 250, "No", self.play_first_buttons)
        self.play_first_buttons[DEFAULT_SELECTION].selected = True

        self.start_button = pygame.Rect(110, 320, START_BUTTON_WIDTH, START_BUTTON_HEIGHT)

    def ask_for_settings(self):
        font = pygame.font.SysFont("Poppins-Regular.ttf", 30)

        while self.running:
            self.screen.fill(BACKGROUND_COLOR)

            for button in self.board_size_buttons:
                button.draw(self.screen)

            for button in self.difficulty_buttons:
                button.draw(self.screen)

            text_surface = font.render(self.play_first_text, True, WHITE)
            self.screen.blit(text_surface, (50, 220))
            for button in self.play_first_buttons:
                button.draw(self.screen)

            pygame.draw.rect(self.screen, BLUE, self.start_button)
            start_text = font.render("Start Game", True, WHITE)
            self.screen.blit(start_text, (self.start_button.x + 10, self.start_button.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for button in self.board_size_buttons:
                    button.handle_event(event)
                for button in self.difficulty_buttons:
                    button.handle_event(event)
                for button in self.play_first_buttons:
                    button.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and self.start_button.collidepoint(event.pos):
                    self.running = False

            pygame.display.flip()

        pygame.quit()

        board_rows, board_columns = self.request_board_size()
        difficulty = self.choose_difficulty()
        user_plays_first = self.want_to_play_first()

        return board_rows, board_columns, difficulty, user_plays_first

    def request_board_size(self):
        for button in self.board_size_buttons:
            if button.is_selected():
                board_size = button.text.split('x')
                return int(board_size[0]), int(board_size[1])
        return 6, 6

    def choose_difficulty(self):
        for button in self.difficulty_buttons:
            if button.is_selected():
                return DIFFICULTY_OPTIONS.index(button.text) + 1
        return 1

    def want_to_play_first(self):
        return self.play_first_buttons[0].is_selected()

# Example usage
# gui = SettingsGUI()
# settings = gui.ask_for_settings()
# print(settings)
