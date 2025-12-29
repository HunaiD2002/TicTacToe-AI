import sys

# 1. Define the ARFF Header
header = """@relation TicTacToe_Complete

@attribute 'top-left-square' {b,o,x}
@attribute 'top-middle-square' {b,o,x}
@attribute 'top-right-square' {b,o,x}
@attribute 'middle-left-square' {b,o,x}
@attribute 'middle-middle-square' {b,o,x}
@attribute 'middle-right-square' {b,o,x}
@attribute 'bottom-left-square' {b,o,x}
@attribute 'bottom-middle-square' {b,o,x}
@attribute 'bottom-right-square' {b,o,x}
@attribute 'Class' {negative,positive}

@data
"""

# 2. Helper Functions
def check_winner(board):
    # Returns 'x', 'o', or None
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != 'b':
            return board[a]
    if 'b' not in board:
        return 'draw'
    return None

memo = {}

def minimax(board, player):
    # Returns 1 if X wins, -1 if O wins, 0 for draw
    board_tuple = tuple(board)
    if board_tuple in memo:
        return memo[board_tuple]
    
    winner = check_winner(board)
    if winner == 'x': return 1
    if winner == 'o': return -1
    if winner == 'draw': return 0

    possibilities = []
    for i in range(9):
        if board[i] == 'b':
            new_board = list(board)
            new_board[i] = player
            score = minimax(new_board, 'o' if player == 'x' else 'x')
            possibilities.append(score)

    if player == 'x':
        res = max(possibilities)
    else:
        res = min(possibilities)
    
    memo[board_tuple] = res
    return res

# 3. Generator Loop
# We use a set to store unique boards strings to avoid duplicates
unique_rows = set()

def generate_all_states(board, player):
    # Determine the "True" outcome of this board
    # If X can force a win from here -> Positive
    # If it's a Draw or O wins -> Negative
    score = minimax(board, player)
    
    # Format for ARFF
    label = "positive" if score == 1 else "negative"
    row_str = ",".join(board) + "," + label
    unique_rows.add(row_str)

    # Continue generating next moves if game not over
    if check_winner(board) is None:
        for i in range(9):
            if board[i] == 'b':
                new_board = list(board)
                new_board[i] = player
                generate_all_states(new_board, 'o' if player == 'x' else 'x')

if __name__ == "__main__":
    print("Generating full dataset... (This may take 10-20 seconds)")
    # Start with empty board, X moves first
    start_board = ['b'] * 9
    generate_all_states(start_board, 'x')

    print(f"Generated {len(unique_rows)} unique board states.")
    
    # Write to file
    with open('resource/full_dataset.arff', 'w') as f:
        f.write(header)
        for row in unique_rows:
            f.write(row + "\n")
            
    print("Done! Saved to resource/full_dataset.arff")