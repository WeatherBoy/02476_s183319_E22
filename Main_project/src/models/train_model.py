# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Script for training the model
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Created by Felix Bo Caspersen, s183319 on Fri Jan 06 2023

# import os

# print(os.getcwd())

import click
import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn import metrics

from src.data.data import mnist
from src.models.model import MyAwesomeModel

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
device = torch.device(DEVICE)  # use cuda or cpu


# Function for finding the accuray given both a target and predictions
def accuracy(target, pred):
    return metrics.accuracy_score(target.detach().cpu().numpy(), pred.detach().cpu().numpy())


LOSS_FUN = torch.nn.CrossEntropyLoss()
NUM_CLASSES = 10


@click.group()
def cli():
    pass


@click.command()
@click.option("--lr", default=1e-3, help="learning rate to use for training")
@click.option("--epochs", default=10, help="Number of epochs to run the training for.")
@click.option("--batch_size", default=32, help="Num batches in training loop.")
@click.option("--validations_per_epoch", default=5, help="Number of validations per epoch.")
@click.option("--save_path", default="best_model.pt", help="Path to save the model.")
def train(lr, epochs, batch_size, validations_per_epoch, save_path):
    # Horrible initialization messages
    print("Training day and night :D")
    print(f"Learning rate: {lr}")
    print(f"Training for {epochs} epochs!")
    print(f"Batch size: {batch_size}")

    best_loss = np.inf

    train_accuracies = []
    train_loss = []

    train_set, _ = mnist()
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)

    model = MyAwesomeModel(NUM_CLASSES)
    model.to(device)
    model.train()

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    N_datapoints = len(train_set)
    # print((N_datapoints // batch_size) // validations_per_epoch)

    for epoch in range(epochs):
        steps = 0

        train_accuracies_batches = []
        train_loss_batches = []

        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            # Forward pass, compute gradients, perform one training step.
            outputs = model(inputs)
            loss = LOSS_FUN(outputs, targets)

            # Zeroing the computational graph
            optimizer.zero_grad()
            loss.backward()

            optimizer.step()

            # Increment step counter
            steps += 1

            # Compute and append accuracy.
            predictions = outputs.max(1)[1]
            train_accuracies_batches.append(accuracy(targets, predictions))

            # append loss
            # detatch it so that it is no longer on the bakcwards graph
            train_loss_batches.append(loss.detach().item())

            # print(f"Steps: {steps}")
            if steps % ((N_datapoints // batch_size) // validations_per_epoch) == 0:

                # Append average training accuracy to list.
                train_accuracies.append(np.mean(train_accuracies_batches))
                train_accuracies_batches = []

                # Append training loss to list

                train_loss.append(np.mean(train_loss_batches))
                train_loss_batches = []

                print(f"Step {batch_size*(steps + epoch*steps):<5}   training accuracy: {train_accuracies[-1]}")
                print(f"Training loss: {train_loss[-1]}")

                if train_loss[-1] < best_loss:
                    best_loss = train_loss[-1]
                    print(f"New best loss: {best_loss} \nModel saved!")
                    torch.save(model.state_dict(), save_path)

        print(f"\nFinished epoch: {epoch + 1}!\n")

    print("\n******************")
    print("Finished training.")
    print("******************")

    plt.figure(figsize=(14, 9))
    plt.title("Learning curves for training")
    plt.plot(train_accuracies, label="Accuracies")
    plt.plot(train_loss, label="Loss")
    plt.legend()
    # plt.show()
    plt.savefig("../../reports/figures/training_curves.png")
    plt.close()


cli.add_command(train)

if __name__ == "__main__":
    cli()
