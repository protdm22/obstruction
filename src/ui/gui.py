import tkinter
from tkinter import messagebox

import pygame

from src.domain.board_exceptions import GameOverException
from src.domain.symbol_types import SymbolTypes

from src.service.game_logic import GameLogic


class GameGUI:
    def __init__(self, game_logic: GameLogic, user_plays_first):
        self.__game_logic = game_logic
        self.__is_user_turn = user_plays_first

    @staticmethod
    def draw_button(cell_text, button_area, screen):

        button_color = (230, 230, 230)
        button_hover_color = (200, 200, 200)
        button_disabled_color = (170, 170, 170)

        font = pygame.font.SysFont('Poppins-Regular.ttf', 50)
        computer_text_color = (255, 50, 50)
        player_text_color = (50, 50, 255)

        if cell_text == SymbolTypes.EMPTY_SYMBOL:
            if button_area.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, button_hover_color, button_area)
            else:
                pygame.draw.rect(screen, button_color, button_area)

        elif cell_text != SymbolTypes.BLOCKED_SYMBOL:
            if cell_text == SymbolTypes.COMPUTER_SYMBOL:
                rendered_text = font.render(cell_text.value, True, computer_text_color)
            else:
                rendered_text = font.render(cell_text.value, True, player_text_color)
            text_rect = rendered_text.get_rect(center=button_area.center)
            pygame.draw.rect(screen, button_color, button_area)
            screen.blit(rendered_text, text_rect)

        else:
            pygame.draw.rect(screen, button_disabled_color, button_area)

    def draw_board(self, game_board, screen):
        button_width, button_height = 50, 50
        button_rectangle_areas = []

        for row_index in range(game_board.rows):
            row_rectangle_area = []
            for column_index in range(game_board.columns):
                button_text = game_board.board[row_index][column_index]
                x_pos = 50 + column_index * (button_width + 10)
                y_pos = 25 + row_index * (button_height + 10)
                button = pygame.Rect(x_pos, y_pos, button_width, button_height)
                row_rectangle_area.append(button)
                self.draw_button(button_text, button, screen)
            button_rectangle_areas.append(row_rectangle_area)
        pygame.display.flip()
        return button_rectangle_areas

    def game_loop(self):
        game_board = self.__game_logic.get_board()
        display_scaling = 2 / 3

        pygame.init()
        screen = pygame.display.set_mode(
            ((game_board.columns * 100 + 65) * display_scaling, (game_board.rows * 100 + 30) * display_scaling))
        pygame.display.set_caption("Obstruction")

        tkinter_window = tkinter.Tk()
        tkinter_window.withdraw()

        button_rectangle_areas = []

        running = True
        while running:
            try:
                if not self.__is_user_turn:
                    pygame.time.wait(250)
                    self.__game_logic.place_computer_symbol()
                    self.__is_user_turn = not self.__is_user_turn

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for row_index in range(game_board.rows):
                            for column_index in range(game_board.columns):
                                button_area = button_rectangle_areas[row_index][column_index]
                                if button_area.collidepoint(event.pos):
                                    if game_board.board[row_index][column_index] == SymbolTypes.EMPTY_SYMBOL:
                                        self.__game_logic.place_player_symbol(row_index, column_index)
                                        self.__is_user_turn = not self.__is_user_turn

                screen.fill((50, 50, 60))
                button_rectangle_areas = self.draw_board(game_board, screen)

            except GameOverException:
                self.draw_board(game_board, screen)
                pygame.time.wait(250)
                if self.__is_user_turn:
                    messagebox.showinfo("Congratulations!", "You won! ╰(*°▽°*)╯")
                else:
                    messagebox.showerror("Womp womp!", "You lost! ಥ_ಥ!")
                running = False

        pygame.quit()
