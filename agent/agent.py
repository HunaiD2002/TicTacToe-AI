import torch
import torch.nn as nn
import torch.nn.functional as F

# 1. ENCODING: Matches the project settings (__init__.py)
#    We define it here to ensure the agent knows how to read 'x', 'o', and 'b' (blank).
ENCODING = {"b": 0, "": 0, " ": 0, "o": -1, "x": 1, "O": -1, "X": 1}

# 2. THE BRAIN (Neural Network)
class TicTacToeNet(nn.Module):
    def __init__(self):
        super(TicTacToeNet, self).__init__()
        # Input: 9 squares
        # Hidden Layers: Increased from 64 to 128 neurons for more brain power!
        self.fc1 = nn.Linear(9, 128) 
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 2)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 3. THE AGENT (The AI Player)
class TicTacToeAgent:
    def __init__(self, model_path=None):
        """
        Initialize the agent and load the brain if a file is provided.
        """
        self.model = TicTacToeNet()
        if model_path:
            try:
                # Load the trained weights
                self.model.load_state_dict(torch.load(model_path))
                self.model.eval() # Set to evaluation mode (not training)
            except Exception as e:
                print(f"Failed to load model: {e}")

    def predict_proba(self, board):
        """
        Predict the probability of a given board state.
        :param board: A list of 9 strings (e.g. ['x', 'b', 'o'...])
        :return: A list of probabilities [prob_negative, prob_positive]
        """
        # Step A: Translate board text to numbers using ENCODING
        encoded_board = [ENCODING.get(cell, 0) for cell in board]
        
        # Step B: Convert to a PyTorch Tensor (floating point numbers)
        input_tensor = torch.tensor(encoded_board, dtype=torch.float32)
        
        # Step C: Ask the Neural Network
        with torch.no_grad():
            output = self.model(input_tensor)
            # Apply Softmax to turn raw scores into percentages (0.0 to 1.0)
            probabilities = F.softmax(output, dim=0)
            
        # Returns something like [0.1, 0.9] (10% chance negative, 90% positive)
        return probabilities.tolist()