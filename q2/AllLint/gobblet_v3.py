"""
Gobblet of Fire: Ignite the Battle

This module implements the game logic and rendering for Gobblet Jr.,
a board game implemented using Pygame.
"""

import pygame
import sys
import os
from typing import List, Tuple, Optional, Dict
import random

# Initialize pygame
pygame.init()

# Constants for the game
SCREEN_HEIGHT = SCREEN_WIDTH = 800
BOARD_SIZE = 3
CELL_SIZE = 100
BOARD_OFFSET = (SCREEN_WIDTH - BOARD_SIZE * CELL_SIZE) // 2
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_RED = (255, 150, 150)
LIGHT_BLUE = (150, 150, 255)
RED_HIGHLIGHT = (255, 87, 51)
RED_BORDER = (183, 28, 28)
BLUE_HIGHLIGHT = (51, 171, 255)
BLUE_BORDER = (13, 71, 161)
GREEN_GLOW = (0, 200, 0, 230)
GREEN_FADE = (100, 255, 100, 150)

# Game text colors
TEXT_COLOR = (240, 240, 240)
PLAYER1_TEXT = (255, 120, 120)
PLAYER2_TEXT = (120, 120, 255)

# Sizes of pieces (radius)
SMALL_SIZE = 10
MEDIUM_SIZE = 25
LARGE_SIZE = 35

# Reserve display settings
RESERVE_SPACING = 95  # Increased from 75 to 120
RESERVE_START_Y = 155
RESERVE_OFFSET_X = 95

# Setup the screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Gobblet of Fire: Ignite the Battle")
clock = pygame.time.Clock()

# Load assets
def load_background():
    """Load and scale the background image; use fallback if unavailable."""
    try:
        bg = pygame.image.load("pic/game-background.jpg").convert()
        return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        # Fallback if image can't be loaded
        print("Warning: Could not load background image. Using fallback.")
        fallback = pygame.Surface(SCREEN_SIZE)
        fallback.fill((40, 40, 40))  # Dark gray fallback
        return fallback

background_texture = load_background()

# Load fonts
title_font = pygame.font.SysFont("arialblack", 36)
game_font = pygame.font.SysFont("arial", 28)
info_font = pygame.font.SysFont("arial", 22)


class Piece:
    """Represents a game piece in Gobblet Jr."""

    def __init__(self, size: int, color: Tuple[int, int, int], player: int):
        """
        Initialize a piece with its size, color, and player.

        Args:
            size: The size of the piece (1=small, 2=medium, 3=large)
            color: RGB color tuple
            player: Player number (1 or 2)
        """
        self.size = size
        self.color = color
        self.player = player
        self.radius = self._get_radius()
        self.selected = False
        self.position = None  # (row, col) or None if not on board
        self.hover = False  # Track if mouse is hovering over this piece

    def _get_radius(self) -> int:
        """Get the radius based on piece size."""
        if self.size == 1:
            return SMALL_SIZE
        elif self.size == 2:
            return MEDIUM_SIZE
        elif self.size == 3:
            return LARGE_SIZE
        else:
            raise ValueError("Invalid piece size")

    def draw(self, screen, x, y, highlight_bool=True):
        """
        Draw the piece at the specified coordinates with optional highlighting.

        Args:
            screen: The Pygame surface to draw on.
            x: X-coordinate.
            y: Y-coordinate.
            highlight_bool: Whether to apply highlighting.
        """
        # Determine the proper colors based on piece state
        if self.color == RED:
            base_color = RED
            highlight_color = RED_HIGHLIGHT if highlight_bool else RED
            border_color = RED_BORDER
        else:  # BLUE
            base_color = BLUE
            highlight_color = BLUE_HIGHLIGHT if highlight_bool else BLUE
            border_color = BLUE_BORDER

        # Add subtle glow effect for selected pieces
        if self.selected:
            glow_radius = self.radius + 5
            pygame.draw.circle(
                screen, (*highlight_color, 150), (x, y), glow_radius
            )
        # Add hover effect
        if self.hover:
            hover_radius = self.radius + 2
            pygame.draw.circle(
                screen, (*highlight_color, 100), (x, y), hover_radius
            )
        # Draw the main piece
        pygame.draw.circle(screen, highlight_color, (x, y), self.radius)
        pygame.draw.circle(
            screen, border_color, (x, y), self.radius, 4
        )  # Border

        # Draw size indicator (dots in the center)
        if self.size == 1:
            pygame.draw.circle(screen, WHITE, (x, y), 3)
        elif self.size == 2:
            pygame.draw.circle(screen, WHITE, (x - 5, y), 3)
            pygame.draw.circle(screen, WHITE, (x + 5, y), 3)
        elif self.size == 3:
            pygame.draw.circle(screen, WHITE, (x, y), 3)
            pygame.draw.circle(screen, WHITE, (x - 7, y), 3)
            pygame.draw.circle(screen, WHITE, (x + 7, y), 3)


class Board:
    """Represents the game board for Gobblet Jr."""

    def __init__(self):
        """Initialize an empty 3x3 board."""
        # Initialize empty board: Each cell can have a stack of pieces
        self.cells = [[[] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.highlight_cell = None  # (row, col) to highlight

    def place_piece(self, piece: Piece, row: int, col: int) -> bool:
        """
        Place a piece on the board at the specified position.

        Returns:
            True if the placement is valid, False otherwise.
        """
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return False

        if self.cells[row][col] and self.cells[row][col][-1].size >= piece.size:
            return False

        piece.position = (row, col)
        self.cells[row][col].append(piece)
        return True

    def remove_piece(self, row: int, col: int) -> Optional[Piece]:
        """
        Remove and return the top piece from the specified position.

        Returns:
            The removed Piece, or None if removal was not possible.
        """
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE) or not self.cells[row][col]:
            return None

        piece = self.cells[row][col].pop()
        piece.position = None
        return piece

    def get_top_piece(self, row: int, col: int) -> Optional[Piece]:
        """
        Get the top piece at the specified position without removing it.

        Returns:
            The top Piece or None if the cell is empty.
        """
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE) or not self.cells[row][col]:
            return None

        return self.cells[row][col][-1]

    def draw(self, screen):
        """Draw the board and all pieces on it."""
        board_surface = pygame.Surface(
            (BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE), pygame.SRCALPHA
        )

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                # Dark blue background
                pygame.draw.rect(board_surface, (10, 15, 30, 180), rect)

                if self.highlight_cell and self.highlight_cell == (row, col):
                    pygame.draw.rect(
                        board_surface, (130, 100, 180, 80), rect
                    )
                # Outer grid lines (purple glow)
                pygame.draw.rect(board_surface, (130, 100, 180), rect, 5)
                pygame.draw.rect(board_surface, (100, 80, 140), rect, 3)
                # Inner grid lines
                rect_inner = rect.copy()
                rect_inner.inflate_ip(-5, -5)
                pygame.draw.rect(
                    board_surface, (100, 80, 140, 150), rect_inner, 2
                )  # Soft purple inner grid

        screen.blit(board_surface, (BOARD_OFFSET, BOARD_OFFSET))

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.cells[row][col]:
                    piece = self.cells[row][col][-1]
                    piece_x = BOARD_OFFSET + col * CELL_SIZE + CELL_SIZE // 2
                    piece_y = BOARD_OFFSET + row * CELL_SIZE + CELL_SIZE // 2
                    piece.draw(screen, piece_x, piece_y)

    def check_win(self, player: int) -> Optional[List[Tuple[int, int]]]:
        """
        Check if the player has won the game.

        Returns:
            A list of winning cell coordinates if there's a win, or None.
        """
        # Check rows
        for row in range(BOARD_SIZE):
            if all(
                self.cells[row][col] and self.cells[row][col][-1].player == player
                for col in range(BOARD_SIZE)
            ):
                return [(row, col) for col in range(BOARD_SIZE)]

        # Check columns
        for col in range(BOARD_SIZE):
            if all(
                self.cells[row][col] and self.cells[row][col][-1].player == player
                for row in range(BOARD_SIZE)
            ):
                return [(row, col) for row in range(BOARD_SIZE)]

        # Check diagonal (top-left to bottom-right)
        if all(
            self.cells[i][i] and self.cells[i][i][-1].player == player
            for i in range(BOARD_SIZE)
        ):
            return [(i, i) for i in range(BOARD_SIZE)]

        # Check diagonal (top-right to bottom-left)
        if all(
            self.cells[i][BOARD_SIZE - 1 - i]
            and self.cells[i][BOARD_SIZE - 1 - i][-1].player == player
            for i in range(BOARD_SIZE)
        ):
            return [(i, BOARD_SIZE - 1 - i) for i in range(BOARD_SIZE)]

        return None


class Game:
    """Main game class for Gobblet Jr."""

    def __init__(self):
        """Initialize a new game."""
        self.board = Board()
        self.current_player = 1
        self.selected_piece = None
        self.player1_reserve = self._create_player_pieces(1, RED)
        self.player2_reserve = self._create_player_pieces(2, BLUE)
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.hover_piece = None
        self.hover_cell = None

        # Animation and transition variables
        self.animation_timer = 0
        self.fade_alpha = 0
        self.show_instructions = True
        self.instruction_fade = 255

        # Initialize button
        self.restart_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 120, 160, 40
        )
        self.button_hover = False

    def _create_player_pieces(
        self, player: int, color: Tuple[int, int, int]
    ) -> List[Piece]:
        """
        Create initial pieces for a player.

        Returns:
            A list of Piece objects.
        """
        pieces = []
        for size in range(1, 4):
            for _ in range(2):
                pieces.append(Piece(size, color, player))
        return pieces

    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click events."""
        if self.game_over:
            if self.restart_button.collidepoint(pos):
                self.restart_game()
            return

        board_rect = pygame.Rect(
            BOARD_OFFSET, BOARD_OFFSET, BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE
        )
        if board_rect.collidepoint(pos):
            board_x = pos[0] - BOARD_OFFSET
            board_y = pos[1] - BOARD_OFFSET
            row = board_y // CELL_SIZE
            col = board_x // CELL_SIZE
            self._handle_board_click(row, col)
            return

        self._handle_reserve_click(pos)

    def _handle_board_click(self, row: int, col: int):
        """Handle click on the board cells."""
        top_piece = self.board.get_top_piece(row, col)
        if not self.selected_piece and top_piece and top_piece.player == self.current_player:
            self.selected_piece = self.board.remove_piece(row, col)
            self.selected_piece.selected = True
        elif self.selected_piece:
            if self.board.place_piece(self.selected_piece, row, col):
                self.selected_piece.selected = False
                self.selected_piece = None
                winning_line = self.board.check_win(self.current_player)
                if winning_line:
                    self.game_over = True
                    self.winner = self.current_player
                    self.winning_line = winning_line
                else:
                    self.current_player = 3 - self.current_player  # Switch player

    def _handle_reserve_click(self, pos: Tuple[int, int]):
        """Handle click on the player's reserve pieces."""
        reserve = (
            self.player1_reserve if self.current_player == 1 
            else self.player2_reserve
        )
        reserve_x = RESERVE_OFFSET_X if self.current_player == 1 else SCREEN_WIDTH - RESERVE_OFFSET_X

        for i, piece in enumerate(reserve):
            piece_y = RESERVE_START_Y + i * RESERVE_SPACING
            distance = ((pos[0] - reserve_x) ** 2 + (pos[1] - piece_y) ** 2) ** 0.5
            if distance <= piece.radius + 10:
                if self.selected_piece:
                    self.selected_piece.selected = False
                    if self.selected_piece.position is not None:
                        row, col = self.selected_piece.position
                        self.board.place_piece(self.selected_piece, row, col)
                    else:
                        (self.player1_reserve if self.selected_piece.player == 1 
                         else self.player2_reserve).append(self.selected_piece)
                self.selected_piece = piece
                self.selected_piece.selected = True
                reserve.remove(piece)
                break

    def handle_motion(self, pos: Tuple[int, int]):
        """Handle mouse motion events for hover effects."""
        self.hover_cell = None
        for piece in self.player1_reserve + self.player2_reserve:
            piece.hover = False

        board_rect = pygame.Rect(
            BOARD_OFFSET, BOARD_OFFSET, BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE
        )
        if board_rect.collidepoint(pos):
            board_x = pos[0] - BOARD_OFFSET
            board_y = pos[1] - BOARD_OFFSET
            row = board_y // CELL_SIZE
            col = board_x // CELL_SIZE
            self.hover_cell = (row, col)
            self.board.highlight_cell = (row, col)
        else:
            self.board.highlight_cell = None

        for player in [1, 2]:
            reserve = (
                self.player1_reserve if player == 1 
                else self.player2_reserve
            )
            reserve_x = RESERVE_OFFSET_X if player == 1 else SCREEN_WIDTH - RESERVE_OFFSET_X
            for i, piece in enumerate(reserve):
                piece_y = RESERVE_START_Y + i * RESERVE_SPACING
                distance = ((pos[0] - reserve_x) ** 2 + (pos[1] - piece_y) ** 2) ** 0.5
                if distance <= piece.radius + 10 and player == self.current_player:
                    piece.hover = True

        self.button_hover = self.restart_button.collidepoint(pos)

    def update(self, dt):
        """Update game state for animations and transitions."""
        if self.show_instructions:
            self.instruction_fade = max(150, self.instruction_fade - 0.5 * dt)
        if self.game_over:
            self.animation_timer += dt
            self.fade_alpha = min(200, self.animation_timer / 10)

    def restart_game(self):
        """Reset the game to its initial state."""
        self.__init__()

    def draw(self, screen):
        """Draw the entire game state."""
        screen.blit(background_texture, (0, 0))
        title_text = "Gobblet of Fire: Ignite the Battle"
        title_surface = title_font.render(title_text, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 35))
        screen.blit(title_surface, title_rect)
        self.board.draw(screen)
        self._draw_reserve(screen)
        if self.selected_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.selected_piece.draw(screen, mouse_x, mouse_y)
        player_text = f"Player {self.current_player}'s Turn"
        text_color = PLAYER1_TEXT if self.current_player == 1 else PLAYER2_TEXT
        if self.game_over:
            player_text = f"Player {self.winner} Wins!"
            text_color = PLAYER1_TEXT if self.winner == 1 else PLAYER2_TEXT
        player_surface = game_font.render(player_text, True, text_color)
        player_rect = player_surface.get_rect(center=(SCREEN_WIDTH // 2, 75))
        screen.blit(player_surface, player_rect)
        if not self.game_over and self.show_instructions:
            instruction = "Select a piece and place it on the board"
            instr_surface = info_font.render(instruction, True, TEXT_COLOR)
            instr_surface.set_alpha(self.instruction_fade)
            instr_rect = instr_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
            )
            screen.blit(instr_surface, instr_rect)
        if self.game_over and self.winning_line:
            self._draw_winning_line(screen)
        if self.game_over:
            button_color = (100, 255, 100) if self.button_hover else (80, 200, 80)
            pygame.draw.rect(screen, button_color, self.restart_button, border_radius=10)
            pygame.draw.rect(
                screen, (30, 100, 30), self.restart_button, 3, border_radius=10
            )
            restart_text = game_font.render("Restart", True, (30, 30, 30))
            restart_rect = restart_text.get_rect(center=self.restart_button.center)
            screen.blit(restart_text, restart_rect)

    def _draw_reserve(self, screen):
        """Draw the reserve pieces for both players."""
        p1_label = game_font.render("Player 1", True, PLAYER1_TEXT)
        p2_label = game_font.render("Player 2", True, PLAYER2_TEXT)
        screen.blit(
            p1_label,
            (
                RESERVE_OFFSET_X - p1_label.get_width() // 2 + 60,
                RESERVE_START_Y - 90,
            ),
        )
        screen.blit(
            p2_label,
            (
                SCREEN_WIDTH - RESERVE_OFFSET_X - p2_label.get_width() // 2 - 60,
                RESERVE_START_Y - 90,
            ),
        )
        for i, piece in enumerate(self.player1_reserve):
            piece_x = RESERVE_OFFSET_X
            piece_y = RESERVE_START_Y + i * RESERVE_SPACING
            pygame.draw.circle(
                screen, (60, 60, 60, 150), (piece_x, piece_y), piece.radius + 5
            )
            piece.draw(screen, piece_x, piece_y, self.current_player == 1)
        for i, piece in enumerate(self.player2_reserve):
            piece_x = SCREEN_WIDTH - RESERVE_OFFSET_X
            piece_y = RESERVE_START_Y + i * RESERVE_SPACING
            pygame.draw.circle(
                screen, (60, 60, 60, 150), (piece_x, piece_y), piece.radius + 5
            )
            piece.draw(screen, piece_x, piece_y, self.current_player == 2)

    def _draw_winning_line(self, screen):
        """Draw a line through the winning cells."""
        line_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        start_row, start_col = self.winning_line[0]
        end_row, end_col = self.winning_line[-1]
        start_x = BOARD_OFFSET + start_col * CELL_SIZE + CELL_SIZE // 2
        start_y = BOARD_OFFSET + start_row * CELL_SIZE + CELL_SIZE // 2
        end_x = BOARD_OFFSET + end_col * CELL_SIZE + CELL_SIZE // 2
        end_y = BOARD_OFFSET + end_row * CELL_SIZE + CELL_SIZE // 2
        highlight_color = PLAYER1_TEXT if self.winner == 1 else PLAYER2_TEXT
        pulse_size = 10 + 5 * (1 + math.sin(self.animation_timer / 100))
        for row, col in self.winning_line:
            cell_x = BOARD_OFFSET + col * CELL_SIZE + CELL_SIZE // 2
            cell_y = BOARD_OFFSET + row * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(
                line_surface,
                (*highlight_color, 100),
                (cell_x, cell_y),
                CELL_SIZE // 2 - pulse_size,
            )
        pygame.draw.line(
            line_surface,
            (*highlight_color, 180),
            (start_x, start_y),
            (end_x, end_y),
            8,
        )
        screen.blit(line_surface, (0, 0))


def main():
    """Main game loop."""
    game = Game()
    previous_time = pygame.time.get_ticks()
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        dt = current_time - previous_time
        previous_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.handle_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                game.handle_motion(event.pos)
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    import math  # Import here to use in the winning animation
    main()
# handled doc strings