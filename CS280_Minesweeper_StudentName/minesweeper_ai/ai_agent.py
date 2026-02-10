"""
Minesweeper AI Agent
Implements intelligent decision-making using logical inference and probabilistic reasoning.
"""

import random


class Sentence:
    """
    Logical statement about a Minesweeper game.
    A sentence consists of a set of board cells and a count of the number of those cells
    which are mines.
    
    For example: {(0,0), (0,1), (1,0)} = 2 means 2 of these 3 cells contain mines.
    """

    def __init__(self, cells, count):
        """
        Initialize a sentence with cells and mine count.
        
        Args:
            cells: Set of tuples (i, j) representing cells
            count: Number of mines among these cells
        """
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        """Check if two sentences are equal."""
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        """String representation of the sentence."""
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        
        If the count equals the number of cells, all cells must be mines.
        """
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        
        If the count is 0, all cells must be safe.
        """
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        
        If the cell is in the sentence, remove it and decrement count.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        
        If the cell is in the sentence, simply remove it.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player using logical inference and probabilistic reasoning.
    """

    def __init__(self, height=8, width=8):
        """
        Initialize AI agent.
        
        Args:
            height: Number of rows in the game
            width: Number of columns in the game
        """
        # Set dimensions
        self.height = height
        self.width = width

        # Keep track of cells that have been clicked
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Mark a cell as a mine and update all knowledge.
        
        Args:
            cell: Tuple (i, j) representing cell coordinates
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Mark a cell as safe and update all knowledge.
        
        Args:
            cell: Tuple (i, j) representing cell coordinates
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us (via revealed cell) that
        a given safe cell has a given number of neighboring mines.
        
        This function should:
        1) Mark the cell as a move that has been made
        2) Mark the cell as safe
        3) Add a new sentence to the AI's knowledge base based on the revealed cell
        4) Mark any additional cells as safe or as mines if it can be concluded
        5) Add any new sentences to the AI's knowledge base if they can be inferred
        
        Args:
            cell: Tuple (i, j) representing the revealed cell
            count: Number of mines adjacent to the cell
        """
        # 1. Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2. Mark the cell as safe
        self.mark_safe(cell)

        # 3. Add a new sentence to the knowledge base
        # Get all neighboring cells
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Skip the cell itself
                if (i, j) == cell:
                    continue
                # Only add valid cells that aren't already known
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) not in self.safes and (i, j) not in self.mines:
                        neighbors.add((i, j))

        # Adjust count for known mines in neighbors
        adjusted_count = count
        neighbors_copy = neighbors.copy()
        for neighbor in neighbors_copy:
            if neighbor in self.mines:
                adjusted_count -= 1
                neighbors.remove(neighbor)

        # Add the new sentence if it has unknown cells
        if len(neighbors) > 0:
            new_sentence = Sentence(neighbors, adjusted_count)
            self.knowledge.append(new_sentence)

        # 4. Iteratively mark additional cells as safe or mines
        self._infer_knowledge()

        # 5. Add new sentences using subset inference
        self._infer_from_subsets()

        # Clean up knowledge base (remove empty sentences)
        self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

    def _infer_knowledge(self):
        """
        Iteratively infer new safe cells and mines from current knowledge.
        Continues until no new information can be inferred.
        """
        knowledge_changed = True
        
        while knowledge_changed:
            knowledge_changed = False
            
            safes_to_mark = set()
            mines_to_mark = set()

            # Check each sentence for definite conclusions
            for sentence in self.knowledge:
                # Find known mines
                known_mines = sentence.known_mines()
                if known_mines:
                    mines_to_mark.update(known_mines)
                    knowledge_changed = True

                # Find known safes
                known_safes = sentence.known_safes()
                if known_safes:
                    safes_to_mark.update(known_safes)
                    knowledge_changed = True

            # Mark all newly identified safe cells
            for safe in safes_to_mark:
                self.mark_safe(safe)

            # Mark all newly identified mines
            for mine in mines_to_mark:
                self.mark_mine(mine)

    def _infer_from_subsets(self):
        """
        Use subset inference to generate new sentences.
        
        If sentence A is a subset of sentence B, we can infer:
        B.cells - A.cells = B.count - A.count
        
        Example:
        {A, B, C} = 2
        {A, B, C, D, E} = 3
        => {D, E} = 1
        """
        new_sentences = []

        for s1 in self.knowledge:
            for s2 in self.knowledge:
                # Skip if same sentence
                if s1 == s2:
                    continue

                # Check if s1 is a subset of s2
                if s1.cells and s2.cells and s1.cells.issubset(s2.cells):
                    # Create new sentence from the difference
                    new_cells = s2.cells - s1.cells
                    new_count = s2.count - s1.count

                    # Only add if it's a valid new sentence
                    if len(new_cells) > 0:
                        new_sentence = Sentence(new_cells, new_count)
                        
                        # Check if this sentence is not already in knowledge
                        if new_sentence not in self.knowledge and new_sentence not in new_sentences:
                            new_sentences.append(new_sentence)

        # Add all new sentences to knowledge base
        self.knowledge.extend(new_sentences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        
        The move must be known to be safe, and not already a move that has been made.
        Returns None if no safe move can be guaranteed.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board using probabilistic reasoning.
        
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
            
        Uses probability calculation to prefer cells with lower mine likelihood.
        """
        # Get all possible moves
        possible_moves = []
        
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    possible_moves.append(cell)

        # If no moves available, return None
        if not possible_moves:
            return None

        # Calculate probabilities for cells involved in knowledge sentences
        cell_probabilities = {}
        
        for sentence in self.knowledge:
            if len(sentence.cells) > 0:
                # Probability that each cell in this sentence is a mine
                prob = sentence.count / len(sentence.cells)
                for cell in sentence.cells:
                    if cell in possible_moves:
                        # Take the maximum probability across all sentences
                        if cell not in cell_probabilities:
                            cell_probabilities[cell] = prob
                        else:
                            cell_probabilities[cell] = max(cell_probabilities[cell], prob)

        # If we have probability information, choose the safest cell
        if cell_probabilities:
            # Find minimum probability
            min_prob = min(cell_probabilities.values())
            safest_moves = [cell for cell, prob in cell_probabilities.items() if prob == min_prob]
            return random.choice(safest_moves)
        
        # Otherwise, choose randomly from all possible moves
        return random.choice(possible_moves)

    def get_knowledge_summary(self):
        """
        Get a summary of the current knowledge state.
        
        Returns:
            Dictionary with knowledge statistics
        """
        return {
            'moves_made': len(self.moves_made),
            'known_safes': len(self.safes),
            'known_mines': len(self.mines),
            'sentences': len(self.knowledge),
            'total_cells_in_sentences': sum(len(s.cells) for s in self.knowledge)
        }
