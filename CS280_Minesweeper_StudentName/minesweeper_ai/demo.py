"""
Enhanced Minesweeper AI Demo
Shows AI capabilities with detailed logging and better first-move strategy.
"""

from minesweeper import Minesweeper
from ai_agent import MinesweeperAI
import random


def run_demo_game():
    """
    Run a single demonstration game with detailed output.
    """
    print("="*70)
    print("MINESWEEPER AI - DETAILED DEMONSTRATION")
    print("="*70)
    
    # Create game
    HEIGHT, WIDTH, MINES = 8, 8, 10
    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
    
    print(f"\nBoard Configuration: {HEIGHT}x{WIDTH} with {MINES} mines")
    print(f"Total cells: {HEIGHT * WIDTH}")
    print(f"Safe cells to reveal: {HEIGHT * WIDTH - MINES}")
    
    # Track game state
    revealed = set()
    move_count = 0
    safe_moves = 0
    random_moves = 0
    
    print("\n" + "-"*70)
    print("GAME START")
    print("-"*70)
    
    # Game loop
    while True:
        move_count += 1
        
        # Get AI knowledge summary
        knowledge = ai.get_knowledge_summary()
        
        print(f"\n{'─'*70}")
        print(f"MOVE #{move_count}")
        print(f"{'─'*70}")
        print(f"Current State:")
        print(f"  • Cells revealed: {len(revealed)}/{HEIGHT * WIDTH - MINES}")
        print(f"  • AI Knowledge: {knowledge['known_safes']} safe cells, "
              f"{knowledge['known_mines']} known mines")
        print(f"  • Active rules: {knowledge['sentences']}")
        
        # Try to make a safe move
        move = ai.make_safe_move()
        if move:
            move_type = "SAFE (Logically certain)"
            safe_moves += 1
        else:
            move = ai.make_random_move()
            move_type = "PROBABILISTIC (Calculated guess)"
            random_moves += 1
        
        # No moves available
        if move is None:
            print(f"\n{'═'*70}")
            print("NO MORE MOVES AVAILABLE")
            print(f"{'═'*70}")
            break
        
        print(f"\nAI Decision: {move_type}")
        print(f"Selected cell: {move}")
        
        # Check if it's a mine
        if game.is_mine(move):
            print(f"\n{'💥'*35}")
            print(f"RESULT: MINE HIT! Game Over.")
            print(f"{'💥'*35}")
            print(f"\nGame Statistics:")
            print(f"  • Total moves made: {move_count}")
            print(f"  • Safe (certain) moves: {safe_moves} ({safe_moves/move_count*100:.1f}%)")
            print(f"  • Probabilistic moves: {random_moves} ({random_moves/move_count*100:.1f}%)")
            print(f"  • Cells successfully revealed: {len(revealed)}")
            print(f"  • Completion: {len(revealed)/(HEIGHT*WIDTH-MINES)*100:.1f}%")
            return False
        
        # Reveal the cell
        revealed.add(move)
        nearby = game.nearby_mines(move)
        
        print(f"RESULT: Safe! ✓")
        print(f"Nearby mines: {nearby}")
        
        # Show which new knowledge was gained
        old_sentence_count = len(ai.knowledge)
        
        # Update AI knowledge
        ai.add_knowledge(move, nearby)
        
        new_sentence_count = len(ai.knowledge)
        
        if nearby > 0:
            print(f"New information added to knowledge base")
            if new_sentence_count > old_sentence_count:
                print(f"  → Generated {new_sentence_count - old_sentence_count} new inference rules")
        
        # Check for win
        if len(revealed) == HEIGHT * WIDTH - MINES:
            print(f"\n{'🎉'*35}")
            print(f"VICTORY! All safe cells revealed!")
            print(f"{'🎉'*35}")
            print(f"\nGame Statistics:")
            print(f"  • Total moves made: {move_count}")
            print(f"  • Safe (certain) moves: {safe_moves} ({safe_moves/move_count*100:.1f}%)")
            print(f"  • Probabilistic moves: {random_moves} ({random_moves/move_count*100:.1f}%)")
            print(f"  • Win efficiency: {(HEIGHT*WIDTH-MINES)/move_count*100:.1f}%")
            return True
    
    return False


def run_multiple_demos(num_games=10):
    """
    Run multiple games and show summary statistics.
    """
    print("\n" + "="*70)
    print(f"RUNNING {num_games} DEMONSTRATION GAMES")
    print("="*70)
    
    wins = 0
    total_moves = 0
    total_safe_moves = 0
    games_completed = []
    
    for i in range(num_games):
        print(f"\n{'▶'*35}")
        print(f"Game {i+1}/{num_games}")
        print(f"{'▶'*35}")
        
        # Run simplified version
        HEIGHT, WIDTH, MINES = 8, 8, 10
        game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
        ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
        
        revealed = set()
        move_count = 0
        safe_move_count = 0
        won = False
        
        while True:
            move_count += 1
            
            # Make move
            move = ai.make_safe_move()
            if move:
                safe_move_count += 1
            else:
                move = ai.make_random_move()
            
            if move is None:
                break
            
            # Check result
            if game.is_mine(move):
                print(f"  Game Over: Mine hit on move {move_count}")
                break
            
            revealed.add(move)
            nearby = game.nearby_mines(move)
            ai.add_knowledge(move, nearby)
            
            # Check win
            if len(revealed) == HEIGHT * WIDTH - MINES:
                print(f"  Victory! Completed in {move_count} moves")
                won = True
                wins += 1
                break
        
        total_moves += move_count
        total_safe_moves += safe_move_count
        games_completed.append({
            'won': won,
            'moves': move_count,
            'safe_moves': safe_move_count
        })
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    print(f"Games played: {num_games}")
    print(f"Wins: {wins} ({wins/num_games*100:.1f}%)")
    print(f"Losses: {num_games - wins} ({(num_games-wins)/num_games*100:.1f}%)")
    print(f"Average moves per game: {total_moves/num_games:.2f}")
    print(f"Average safe moves: {total_safe_moves/num_games:.2f}")
    print(f"Safe move percentage: {total_safe_moves/total_moves*100:.1f}%")
    print("="*70)


def demonstrate_inference():
    """
    Show a step-by-step example of AI inference.
    """
    print("\n" + "="*70)
    print("INFERENCE ENGINE DEMONSTRATION")
    print("="*70)
    
    ai = MinesweeperAI(height=8, width=8)
    
    print("\nScenario: AI reveals cell (3,3) and sees 2 nearby mines")
    print("\nStep 1: Create initial sentence")
    
    # Simulate revealing a cell
    cell = (3, 3)
    count = 2
    
    # Get neighbors
    neighbors = []
    for i in range(cell[0] - 1, cell[0] + 2):
        for j in range(cell[1] - 1, cell[1] + 2):
            if (i, j) != cell and 0 <= i < 8 and 0 <= j < 8:
                neighbors.append((i, j))
    
    print(f"  Initial knowledge: {set(neighbors)} = {count}")
    print(f"  (2 of these {len(neighbors)} cells contain mines)")
    
    # Add knowledge
    ai.add_knowledge(cell, count)
    
    print(f"\nStep 2: After inference")
    print(f"  Knowledge base has {len(ai.knowledge)} sentences")
    
    # Simulate more moves to show inference
    print(f"\nScenario: AI reveals cell (2,2) and sees 1 nearby mine")
    ai.add_knowledge((2, 2), 1)
    
    print(f"  Knowledge base now has {len(ai.knowledge)} sentences")
    print(f"  Known safe cells: {len(ai.safes)}")
    print(f"  Known mines: {len(ai.mines)}")
    
    print("\nThis demonstrates how the AI:")
    print("  ✓ Creates logical sentences from observations")
    print("  ✓ Combines sentences to infer new information")
    print("  ✓ Identifies safe cells and mines with certainty")
    print("  ✓ Builds knowledge progressively")


if __name__ == "__main__":
    # Run single detailed demo
    print("\n" + "🤖 "*35)
    run_demo_game()
    
    # Show inference demonstration
    demonstrate_inference()
    
    # Run multiple games
    run_multiple_demos(20)
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nKey Observations:")
    print("  • The AI uses logical inference to identify safe moves")
    print("  • When certainty isn't possible, it uses probability")
    print("  • Performance depends on board configuration and luck")
    print("  • The knowledge base grows and becomes more powerful over time")
    print("="*70 + "\n")
