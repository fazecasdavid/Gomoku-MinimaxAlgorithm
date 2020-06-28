import pygame
from Exceptions import *
import utils


class Graphical:
    def __init__(self, service):
        self._service = service
        self._screen = None
        self.on_init()

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode((45*self._service.get_length(), 45*self._service.get_length()))
        pygame.display.set_caption("Gomoku")

    def draw_board(self):
        board = self._service.get_board()
        for c in range(len(board)):
            for r in range(len(board)):
                pygame.draw.rect(self._screen, (120, 96, 66), (c * 45, r * 45, 45, 45))
                pygame.draw.rect(self._screen, (0, 0, 0), (c * 45, r * 45, 45, 45), 1)

        for c in range(len(board)):
            for r in range(len(board)):
                if board[c][r] == 1:
                    pygame.draw.circle(self._screen, (59, 47, 31), (c*45 + 45//2, r*45 + 45//2), 45//2-3)
                elif board[c][r] == -1:
                    pygame.draw.circle(self._screen, (255, 210, 166), (c*45 + 45//2, r*45 + 45//2), 45//2-3)
        pygame.display.update()

    def start(self):
        game_over = False

        while not game_over:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self._service.get_turn() == 1:
                        try:
                            x = event.pos[0] // 45
                            y = event.pos[1] // 45
                            self._service.player_move(x, y)
                            if utils.game_over(self._service.get_board(), 1):
                                game_over = True
                        except Exceptions:
                            continue
            self.draw_board()
            if not game_over and self._service.get_turn() == -1:
                self._service.computer_move()
                if utils.game_over(self._service.get_board(), -1):
                    game_over = True

        self.draw_board()
        font = pygame.font.Font('freesansbold.ttf', 70)

        if self._service.get_turn() == -1:
            text = font.render('You Won!', True, (0, 0, 143))
            text_rect = text.get_rect()
            text_rect.center = (45*self._service.get_length()//2, 45*self._service.get_length()//2)
            self._screen.blit(text, text_rect)
        elif self._service.get_turn() == 1:
            text = font.render('You Lost!', True, (0, 0, 150))
            text_rect = text.get_rect()
            text_rect.center = (45*self._service.get_length()//2, 45*self._service.get_length()//2)
            self._screen.blit(text, text_rect)

        pygame.display.update()

        r = True
        while r:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    r = False
        pygame.quit()


