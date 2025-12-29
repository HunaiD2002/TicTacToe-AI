# Unbeatable Tic-Tac-Toe AI 🎮🧠

An advanced Tic-Tac-Toe agent built with **Python** and **PyTorch**. This project demonstrates how to combine Deep Learning with game theory (Minimax) and rule-based logic to create an opponent that cannot be beaten.

## 🚀 Key Features
* **Neural Network Brain:** A Feed-Forward Neural Network trained to predict winning probabilities for any given board state.
* **Perfect Training Data:** Includes a custom script (`generate_dataset.py`) that uses the **Minimax algorithm** to generate the entire game tree (every possible legal move), ensuring the AI has seen every scenario.
* **Hybrid Intelligence:**
    * **Reflex Layer:** Hard-coded logic to instantly spot immediate wins or blocks.
    * **Strategic Layer:** The Neural Network handles complex mid-game positioning.
* **"Killer Mode" (Perspective Swap):** The agent actively calculates its own winning probability (Aggressive) rather than just minimizing the opponent's winning chance (Defensive).

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/HunaiD2002/TicTacToe-AI.git] (https://github.com/YOUR_USERNAME/TicTacToe-AI.git)
    cd TicTacToe-AI
    ```

2.  **Install dependencies:**
    ```bash
    pip install torch numpy pandas
    ```

## 🏃‍♂️ How to Run

### Step 1: Generate the Data
Instead of using a limited dataset, run this script to generate a perfect dataset containing every possible game state using Minimax.
```bash
python generate_dataset.py


MIT License

Copyright (c) 2025 Hunaid Barodawala

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.   