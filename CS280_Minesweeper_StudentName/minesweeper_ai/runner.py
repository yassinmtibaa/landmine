"""
Minesweeper Game Runner with Pygame Visualization
Provides interactive GUI for playing Minesweeper and watching the AI agent.
"""

import pygame
import sys
import time
from minesweeper import Minesweeper
from ai_agent import MinesweeperAI

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (220, 220, 220)

# Game settings
HEIGHT = 8
WIDTH = 8
MINES = 10

# Display settings
BOARD_PADDING = 20
CELL_SIZE = 50
CELL_SPACING = 2
FLAG_FONT_SIZE = 30
NUMBER_FONT_SIZE = 28
INSTRUCTION_FONT_SIZE = 20


def main():
    """Main game loop with pygame visualization."""
    
    # Initialize pygame
    pygame.init()
    
    # Calculate display dimensions
    board_width = (WIDTH * (CELL_SIZE + CELL_SPACING)) - CELL_SPACING
    board_height = (HEIGHT * (CELL_SIZE + CELL_SPACING)) - CELL_SPACING
    
    width = board_width + 2 * BOARD_PADDING
    height = board_height + 2 * BOARD_PADDING + 130
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Minesweeper AI")

    # Fonts
    flag_font = pygame.font.Font(None, FLAG_FONT_SIZE)
    number_font = pygame.font.Font(None, NUMBER_FONT_SIZE)
    instruction_font = pygame.font.Font(None, INSTRUCTION_FONT_SIZE)
    medium_font = pygame.font.Font(None, 24)

    # Create game and AI agent
    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

    # Track revealed cells and flagged cells
    revealed = set()
    flags = set()
    lost = False
    
    # AI play variables
    ai_playing = False
    ai_move_delay = 0.3  # seconds between AI moves

    # Instructions
    instructions = True

    while True:
        # Check for game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # Show instructions initially
        if instructions:
            # Title
            title = medium_font.render("Play Minesweeper", True, WHITE)
            title_rect = title.get_rect()
            title_rect.center = (width / 2, 50)
            screen.blit(title, title_rect)

            # Rules
            rules = [
                "Click a cell to reveal it.",
                "Right-click a cell to mark it as a mine.",
                "Mark all mines successfully to win!",
                "",
                "Press any key to start..."
            ]
            for i, rule in enumerate(rules):
                line = instruction_font.render(rule, True, WHITE)
                line_rect = line.get_rect()
                line_rect.center = (width / 2, 150 + 30 * i)
                screen.blit(line, line_rect)

            pygame.display.flip()

            # Wait for key press
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        waiting = False
                        instructions = False

            continue

        # Draw board
        cells = []
        for i in range(HEIGHT):
            row = []
            for j in range(WIDTH):
                # Calculate cell position
                rect = pygame.Rect(
                    BOARD_PADDING + j * (CELL_SIZE + CELL_SPACING),
                    BOARD_PADDING + i * (CELL_SIZE + CELL_SPACING),
                    CELL_SIZE, CELL_SIZE
                )

                # Color cell based on state
                if (i, j) in revealed:
                    # Revealed cell
                    if game.is_mine((i, j)):
                        # Mine - red
                        pygame.draw.rect(screen, RED, rect)
                        pygame.draw.rect(screen, DARK_GRAY, rect, 2)
                        # Draw mine symbol
                        mine_text = flag_font.render("💣", True, BLACK)
                        mine_rect = mine_text.get_rect()
                        mine_rect.center = rect.center
                        screen.blit(mine_text, mine_rect)
                    else:
                        # Safe cell
                        pygame.draw.rect(screen, LIGHT_GRAY, rect)
                        pygame.draw.rect(screen, DARK_GRAY, rect, 2)
                        # Show number of nearby mines
                        nearby = game.nearby_mines((i, j))
                        if nearby > 0:
                            # Color based on number
                            colors = [None, BLUE, GREEN, RED, (128, 0, 128), 
                                    (255, 140, 0), (0, 128, 128), BLACK, DARK_GRAY]
                            number_text = number_font.render(str(nearby), True, colors[nearby])
                            number_rect = number_text.get_rect()
                            number_rect.center = rect.center
                            screen.blit(number_text, number_rect)
                elif (i, j) in flags:
                    # Flagged cell
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.rect(screen, DARK_GRAY, rect, 2)
                    flag_text = flag_font.render("🚩", True, RED)
                    flag_rect = flag_text.get_rect()
                    flag_rect.center = rect.center
                    screen.blit(flag_text, flag_rect)
                else:
                    # Unrevealed cell
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.rect(screen, DARK_GRAY, rect, 2)

                row.append(rect)
            cells.append(row)

        # Draw buttons
        button_y = board_height + 2 * BOARD_PADDING + 10
        
        # AI Move button
        ai_button = pygame.Rect(BOARD_PADDING, button_y, 150, 35)
        ai_button_text = "AI Move" if not ai_playing else "Stop AI"
        button_color = GREEN if not ai_playing else RED
        pygame.draw.rect(screen, button_color, ai_button)
        ai_text = instruction_font.render(ai_button_text, True, WHITE)
        ai_text_rect = ai_text.get_rect()
        ai_text_rect.center = ai_button.center
        screen.blit(ai_text, ai_text_rect)

        # Reset button
        reset_button = pygame.Rect(BOARD_PADDING + 160, button_y, 100, 35)
        pygame.draw.rect(screen, DARK_GRAY, reset_button)
        reset_text = instruction_font.render("Reset", True, WHITE)
        reset_text_rect = reset_text.get_rect()
        reset_text_rect.center = reset_button.center
        screen.blit(reset_text, reset_text_rect)

        # Display game status
        status_text = ""
        status_color = WHITE
        
        if lost:
            status_text = "Game Over - Mine Hit!"
            status_color = RED
        elif game.mines == flags:
            status_text = "Victory!"
            status_color = GREEN
        else:
            status_text = f"Mines: {MINES} | Flags: {len(flags)} | Revealed: {len(revealed)}"
            
        status = instruction_font.render(status_text, True, status_color)
        status_rect = status.get_rect()
        status_rect.center = (width / 2, button_y + 55)
        screen.blit(status, status_rect)

        # AI knowledge display
        ai_info = ai.get_knowledge_summary()
        ai_status = instruction_font.render(
            f"AI: {ai_info['known_safes']} safes, {ai_info['known_mines']} mines, "
            f"{ai_info['sentences']} rules",
            True, BLUE
        )
        ai_status_rect = ai_status.get_rect()
        ai_status_rect.center = (width / 2, button_y + 80)
        screen.blit(ai_status, ai_status_rect)

        pygame.display.flip()

        # Handle AI playing
        if ai_playing and not lost and game.mines != flags:
            time.sleep(ai_move_delay)
            
            # Try to make a safe move
            move = ai.make_safe_move()
            if move is None:
                # No safe move, make a random move
                move = ai.make_random_move()
                if move is None:
                    # No moves left
                    ai_playing = False
                    continue

            # Make the move
            if move:
                if game.is_mine(move):
                    lost = True
                    ai_playing = False
                else:
                    nearby = game.nearby_mines(move)
                    revealed.add(move)
                    ai.add_knowledge(move, nearby)

            continue

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if AI button clicked
                if ai_button.collidepoint(mouse_pos):
                    if not lost and game.mines != flags:
                        ai_playing = not ai_playing
                
                # Check if reset button clicked
                elif reset_button.collidepoint(mouse_pos):
                    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                    revealed = set()
                    flags = set()
                    lost = False
                    ai_playing = False
                
                # Check if a cell was clicked
                elif not lost and game.mines != flags:
                    for i in range(HEIGHT):
                        for j in range(WIDTH):
                            if cells[i][j].collidepoint(mouse_pos):
                                # Left click - reveal
                                if event.button == 1:
                                    if (i, j) not in flags and (i, j) not in revealed:
                                        if game.is_mine((i, j)):
                                            lost = True
                                        else:
                                            nearby = game.nearby_mines((i, j))
                                            revealed.add((i, j))
                                            ai.add_knowledge((i, j), nearby)
                                
                                # Right click - flag
                                elif event.button == 3:
                                    if (i, j) not in revealed:
                                        if (i, j) in flags:
                                            flags.remove((i, j))
                                        else:
                                            flags.add((i, j))
                                            ai.mark_mine((i, j))


if __name__ == "__main__":
    main()
