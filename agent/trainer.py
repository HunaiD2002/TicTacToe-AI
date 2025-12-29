import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import os

from util.data_loader import load_arff_dataset
from util.dataset import TicTacToeDataset
from agent.agent import TicTacToeNet

def train_agent(data_path, output_path, epochs, load_path=None):
    print(f"Loading data from {data_path}...")
    try:
        X, y = load_arff_dataset(data_path)
    except Exception as e:
        print(f"Error loading ARFF file: {e}")
        return

    dataset = TicTacToeDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Initializing the network
    model = TicTacToeNet()

    # NEW: Load existing model (if provided)
    if load_path and os.path.exists(load_path):
        print(f"Resuming training from {load_path}...")
        model.load_state_dict(torch.load(load_path))
    else:
        print("Initializing new model from scratch...")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print(f"Starting training for {epochs} epochs...")
    model.train()

    best_accuracy = 0.0

    for epoch in range(epochs):
        correct = 0
        total_samples = 0
        total_loss = 0
        
        for batch_X, batch_y in dataloader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_samples += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()

        # accuracy for this epoch
        current_accuracy = 100 * correct / total_samples

        # NEW: Only save if this is the best version 
        if current_accuracy > best_accuracy:
            best_accuracy = current_accuracy
            torch.save(model.state_dict(), output_path)
            
        if (epoch + 1) % 50 == 0:
            print(f'Epoch [{epoch+1}/{epochs}] | Loss: {total_loss:.4f} | Acc: {current_accuracy:.2f}% | Best: {best_accuracy:.2f}%')
            
    print(f"Training complete. Best model saved to {output_path} with {best_accuracy:.2f}% accuracy.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--epochs', type=int, default=500)
    # NEW argument: --load
    parser.add_argument('--load', type=str, default=None, help="Path to existing model to continue training")
    args = parser.parse_args()

    train_agent(args.data, args.out, args.epochs, args.load)