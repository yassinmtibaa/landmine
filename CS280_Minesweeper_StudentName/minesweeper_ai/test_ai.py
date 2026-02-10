"""
Minesweeper AI Testing and Evaluation Framework
Runs multiple games to evaluate AI performance and generate statistics.
"""

import random
from minesweeper import Minesweeper
from ai_agent import MinesweeperAI
from collections import defaultdict
import json


class MinesweeperTester:
    """
    Testing framework for evaluating Minesweeper AI performance.
    """

    def __init__(self):
        """Initialize the tester."""
        self.results = []

    def run_single_game(self, height, width, mines, verbose=False):
        """
        Run a single game and return the result.
        
        Args:
            height: Board height
            width: Board width
            mines: Number of mines
            verbose: Print detailed game progress
            
        Returns:
            Dictionary with game statistics
        """
        game = Minesweeper(height=height, width=width, mines=mines)
        ai = MinesweeperAI(height=height, width=width)
        
        revealed = set()
        flags = set()
        move_count = 0
        safe_moves = 0
        random_moves = 0
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"Starting game: {height}x{width} with {mines} mines")
            print(f"{'='*60}")
        
        # Game loop
        while True:
            move_count += 1
            
            # Try safe move first
            move = ai.make_safe_move()
            if move:
                safe_moves += 1
                move_type = "SAFE"
            else:
                # Make random move
                move = ai.make_random_move()
                random_moves += 1
                move_type = "RANDOM"
            
            # No moves available
            if move is None:
                if verbose:
                    print(f"No more moves available")
                break
            
            if verbose:
                knowledge = ai.get_knowledge_summary()
                print(f"\nMove {move_count} ({move_type}): {move}")
                print(f"  Knowledge: {knowledge['known_safes']} safe, "
                      f"{knowledge['known_mines']} mines, {knowledge['sentences']} rules")
            
            # Check if it's a mine
            if game.is_mine(move):
                if verbose:
                    print(f"  Result: HIT A MINE! Game Over.")
                return {
                    'won': False,
                    'moves': move_count,
                    'safe_moves': safe_moves,
                    'random_moves': random_moves,
                    'height': height,
                    'width': width,
                    'mines': mines,
                    'revealed': len(revealed),
                    'accuracy': safe_moves / move_count if move_count > 0 else 0
                }
            
            # Reveal the cell
            revealed.add(move)
            nearby = game.nearby_mines(move)
            
            if verbose:
                print(f"  Result: Safe! {nearby} nearby mines")
            
            # Update AI knowledge
            ai.add_knowledge(move, nearby)
            
            # Check for win (all non-mine cells revealed)
            total_cells = height * width
            if len(revealed) == total_cells - mines:
                if verbose:
                    print(f"\n{'='*60}")
                    print(f"VICTORY! All safe cells revealed!")
                    print(f"{'='*60}")
                return {
                    'won': True,
                    'moves': move_count,
                    'safe_moves': safe_moves,
                    'random_moves': random_moves,
                    'height': height,
                    'width': width,
                    'mines': mines,
                    'revealed': len(revealed),
                    'accuracy': safe_moves / move_count if move_count > 0 else 0
                }
        
        # Game ended without win or loss (no moves available)
        return {
            'won': False,
            'moves': move_count,
            'safe_moves': safe_moves,
            'random_moves': random_moves,
            'height': height,
            'width': width,
            'mines': mines,
            'revealed': len(revealed),
            'accuracy': safe_moves / move_count if move_count > 0 else 0
        }

    def run_multiple_games(self, height, width, mines, num_games=100, verbose=False):
        """
        Run multiple games and collect statistics.
        
        Args:
            height: Board height
            width: Board width
            mines: Number of mines
            num_games: Number of games to run
            verbose: Print progress
            
        Returns:
            Dictionary with aggregated statistics
        """
        wins = 0
        total_moves = 0
        total_safe_moves = 0
        total_random_moves = 0
        total_revealed = 0
        
        print(f"\nRunning {num_games} games on {height}x{width} board with {mines} mines...")
        
        for i in range(num_games):
            if verbose or (i + 1) % 10 == 0:
                print(f"  Game {i + 1}/{num_games}...", end='\r')
            
            result = self.run_single_game(height, width, mines, verbose=False)
            self.results.append(result)
            
            if result['won']:
                wins += 1
            total_moves += result['moves']
            total_safe_moves += result['safe_moves']
            total_random_moves += result['random_moves']
            total_revealed += result['revealed']
        
        print()  # New line after progress
        
        # Calculate statistics
        win_rate = (wins / num_games) * 100
        avg_moves = total_moves / num_games
        avg_safe_moves = total_safe_moves / num_games
        avg_random_moves = total_random_moves / num_games
        avg_revealed = total_revealed / num_games
        avg_accuracy = (total_safe_moves / total_moves * 100) if total_moves > 0 else 0
        
        stats = {
            'configuration': f"{height}x{width} with {mines} mines",
            'games_played': num_games,
            'wins': wins,
            'losses': num_games - wins,
            'win_rate': win_rate,
            'avg_moves': avg_moves,
            'avg_safe_moves': avg_safe_moves,
            'avg_random_moves': avg_random_moves,
            'avg_revealed_cells': avg_revealed,
            'avg_accuracy': avg_accuracy
        }
        
        return stats

    def print_statistics(self, stats):
        """
        Print formatted statistics.
        
        Args:
            stats: Statistics dictionary from run_multiple_games
        """
        print(f"\n{'='*70}")
        print(f"MINESWEEPER AI PERFORMANCE REPORT")
        print(f"{'='*70}")
        print(f"Configuration: {stats['configuration']}")
        print(f"Games Played:  {stats['games_played']}")
        print(f"-" * 70)
        print(f"Wins:          {stats['wins']}")
        print(f"Losses:        {stats['losses']}")
        print(f"Win Rate:      {stats['win_rate']:.2f}%")
        print(f"-" * 70)
        print(f"Average Moves per Game:        {stats['avg_moves']:.2f}")
        print(f"Average Safe Moves:            {stats['avg_safe_moves']:.2f}")
        print(f"Average Random/Probabilistic:  {stats['avg_random_moves']:.2f}")
        print(f"Average Cells Revealed:        {stats['avg_revealed_cells']:.2f}")
        print(f"Safe Move Accuracy:            {stats['avg_accuracy']:.2f}%")
        print(f"{'='*70}\n")

    def run_difficulty_comparison(self):
        """
        Compare AI performance across different difficulty levels.
        """
        print("\n" + "="*70)
        print("COMPREHENSIVE DIFFICULTY COMPARISON")
        print("="*70)
        
        # Different difficulty configurations
        configurations = [
            # Easy
            {'name': 'Beginner (8x8, 10 mines)', 'height': 8, 'width': 8, 'mines': 10, 'games': 100},
            # Medium
            {'name': 'Intermediate (16x16, 40 mines)', 'height': 16, 'width': 16, 'mines': 40, 'games': 50},
            # Hard
            {'name': 'Expert (16x30, 99 mines)', 'height': 16, 'width': 30, 'mines': 99, 'games': 25},
            # Custom tests
            {'name': 'Small Dense (5x5, 8 mines)', 'height': 5, 'width': 5, 'mines': 8, 'games': 100},
            {'name': 'Large Sparse (20x20, 50 mines)', 'height': 20, 'width': 20, 'mines': 50, 'games': 25},
        ]
        
        all_stats = []
        
        for config in configurations:
            print(f"\nTesting: {config['name']}")
            stats = self.run_multiple_games(
                config['height'], 
                config['width'], 
                config['mines'], 
                config['games']
            )
            stats['name'] = config['name']
            all_stats.append(stats)
            self.print_statistics(stats)
        
        # Summary comparison
        print("\n" + "="*70)
        print("SUMMARY COMPARISON")
        print("="*70)
        print(f"{'Difficulty':<35} {'Win Rate':<15} {'Avg Moves':<15}")
        print("-" * 70)
        for stats in all_stats:
            print(f"{stats['name']:<35} {stats['win_rate']:>6.2f}%        {stats['avg_moves']:>7.2f}")
        print("="*70 + "\n")
        
        return all_stats

    def save_results(self, filename='test_results.json'):
        """
        Save all test results to a JSON file.
        
        Args:
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filename}")


def main():
    """Run comprehensive AI testing."""
    tester = MinesweeperTester()
    
    print("="*70)
    print("MINESWEEPER AI - COMPREHENSIVE TESTING SUITE")
    print("="*70)
    
    # Option 1: Run a single visible game
    print("\n[1] Running a single game with detailed output...")
    result = tester.run_single_game(8, 8, 10, verbose=True)
    
    # Option 2: Run standard test suite
    print("\n[2] Running standard test suite (Beginner level)...")
    stats = tester.run_multiple_games(8, 8, 10, num_games=100)
    tester.print_statistics(stats)
    
    # Option 3: Run comprehensive difficulty comparison
    print("\n[3] Running comprehensive difficulty comparison...")
    all_stats = tester.run_difficulty_comparison()
    
    # Save results
    # tester.save_results()
    
    print("\n✓ Testing complete!")


if __name__ == "__main__":
    main()
