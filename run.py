import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from machine import Machine

# Define the parameter sets to iterate over with smaller values
parameter_sets = [
    (3, 50, 9, 'hebbian'),
    (3, 50, 10, 'hebbian'),
    (3, 50, 11, 'hebbian'),
    (3, 50, 12, 'hebbian'),
    (3, 50, 13, 'hebbian'),
    (4, 50, 9, 'hebbian'),
    (4, 50, 10, 'hebbian'),
    (4, 50, 11, 'hebbian'),
    (4, 50, 12, 'hebbian'),
    (4, 50, 13, 'hebbian'),
    (5, 50, 9, 'hebbian'),
    (5, 50, 10, 'hebbian'),
    (5, 50, 11, 'hebbian'),
    (5, 50, 12, 'hebbian'),
    (5, 50, 13, 'hebbian'),
    (3, 50, 9, 'anti_hebbian'),
    (3, 50, 10, 'anti_hebbian'),
    (3, 50, 11, 'anti_hebbian'),
    (3, 50, 12, 'anti_hebbian'),
    (3, 50, 13, 'anti_hebbian'),
    (4, 50, 9, 'anti_hebbian'),
    (4, 50, 10, 'anti_hebbian'),
    (4, 50, 11, 'anti_hebbian'),
    (4, 50, 12, 'anti_hebbian'),
    (4, 50, 13, 'anti_hebbian'),
    (5, 50, 9, 'anti_hebbian'),
    (5, 50, 10, 'anti_hebbian'),
    (5, 50, 11, 'anti_hebbian'),
    (5, 50, 12, 'anti_hebbian'),
    (5, 50, 13, 'anti_hebbian'),
    (3, 50, 9, 'random_walk'),
    (3, 50, 10, 'random_walk'),
    (3, 50, 11, 'random_walk'),
    (3, 50, 12, 'random_walk'),
    (3, 50, 13, 'random_walk'),
    (4, 50, 9, 'random_walk'),
    (4, 50, 10, 'random_walk'),
    (4, 50, 11, 'random_walk'),
    (4, 50, 12, 'random_walk'),
    (4, 50, 13, 'random_walk'),
    (5, 50, 9, 'random_walk'),
    (5, 50, 10, 'random_walk'),
    (5, 50, 11, 'random_walk'),
    (5, 50, 12, 'random_walk'),
    (5, 50, 13, 'random_walk')
]


# Function to generate random number
def random(l, k, n):
    return np.random.randint(-l, l + 1, [k, n])

# Function to evaluate the synchronization score between two machines
def sync_score(m1, m2, l):
    return np.sum(m1.W == m2.W) / (m1.k * m1.n)

# Function to run the synchronization process and log results
def run_simulation(k, n, l, update_rule, num_simulations):
    simple_attack_success = 0
    majority_attack_success = 0
    no_sync_success = 0
    sync_only_AB_success = 0
    sync_ABE_success = 0

    for _ in range(num_simulations):
        Alice = Machine(k, n, l)
        Bob = Machine(k, n, l)
        Eve = Machine(k, n, l)

        sync = False
        nb_updates = 0
        nb_eve_updates = 0

        while not sync:
            X = random(l, k, n)
            tauA = Alice(X)
            tauB = Bob(X)
            tauE = Eve(X)

            Alice.update(tauB, update_rule)
            Bob.update(tauA, update_rule)

            if tauA == tauB == tauE:
                Eve.update(tauA, update_rule)
                nb_eve_updates += 1

            nb_updates += 1
            score = 100 * sync_score(Alice, Bob, l)

            if score == 100:
                sync = True

            # Check additional conditions
            if tauA != tauB:  # Condition: τA ≠ τB
                no_sync_success += 1
                break

            if tauA == tauB != tauE:  # Condition: τA = τB ≠ τC
                sync_only_AB_success += 1
                break

            if tauA == tauB == tauE:  # Condition: τA = τB = τC
                sync_ABE_success += 1
                break

        # Calculate simple attack success
        eve_score = 100 * sync_score(Alice, Eve, l)
        if eve_score == 100:
            simple_attack_success += 1

        # Calculate majority attack success
        if nb_eve_updates > (nb_updates / 2):
            majority_attack_success += 1

    # Calculate probabilities
    simple_attack_prob = simple_attack_success / num_simulations
    majority_attack_prob = majority_attack_success / num_simulations
    no_sync_prob = no_sync_success / num_simulations
    sync_only_AB_prob = sync_only_AB_success / num_simulations
    sync_ABE_prob = sync_ABE_success / num_simulations

    return simple_attack_prob, majority_attack_prob, no_sync_prob, sync_only_AB_prob, sync_ABE_prob

# Function to print results in a tabular format
# Function to print results in a tabular format
def print_table(parameter_sets, results):
    print("| {:<3} | {:<3} | {:<3} | {:<13} | {:<16} | {:<18} | {:<11} | {:<16} | {:<11} |".format("k", "n", "l", "Update Rule", "Simple Attack", "Majority Attack", "No Sync", "Sync AB Only", "Sync ABE"))
    print("|" + "-"*5 + "|" + "-"*5 + "|" + "-"*5 + "|" + "-"*15 + "|" + "-"*17 + "|" + "-"*19 + "|" + "-"*12 + "|" + "-"*17 + "|" + "-"*12 + "|")
    for i, params in enumerate(parameter_sets):
        k, n, l, update_rule = params
        simple_attack_prob, majority_attack_prob, no_sync_prob, sync_only_AB_prob, sync_ABE_prob = results[i]
        print("| {:<3} | {:<3} | {:<3} | {:<13} | {:<16.2f} | {:<18.2f} | {:<11.2f} | {:<16.2f} | {:<11.2f} |".format(k, n, l, update_rule, simple_attack_prob, majority_attack_prob, no_sync_prob, sync_only_AB_prob, sync_ABE_prob))

# Function to plot results
# Function to plot results
def plot_results(parameter_sets, results):
    simple_attack_probs = [result[0] for result in results]
    majority_attack_probs = [result[1] for result in results]
    no_sync_probs = [result[2] for result in results]
    sync_only_AB_probs = [result[3] for result in results]
    sync_ABE_probs = [result[4] for result in results]

    parameter_labels = [f"{k}-{n}-{l}-{rule}" for k, n, l, rule in parameter_sets]

    # Create a new figure
    plt.figure(figsize=(14, 10))

    # Plot simple attack probabilities
    plt.subplot(2, 3, 1)
    plt.plot(simple_attack_probs, label="Simple Attack Probability", marker='o')
    plt.xticks(range(len(parameter_labels)), parameter_labels, rotation=45, ha="right")
    plt.xlabel("Parameter Set Index")
    plt.ylabel("Probability")
    plt.title("Simple Attack Success Probability")
    plt.legend()

    # Plot majority attack probabilities
    plt.subplot(2, 3, 2)
    plt.plot(majority_attack_probs, label="Majority Attack Probability", marker='o')
    plt.xticks(range(len(parameter_labels)), parameter_labels, rotation=45, ha="right")
    plt.xlabel("Parameter Set Index")
    plt.ylabel("Probability")
    plt.title("Majority Attack Success Probability")
    plt.legend()

    # Plot no synchronization probabilities
    plt.subplot(2, 3, 3)
    plt.plot(no_sync_probs, label="No Sync Probability", marker='o')
    plt.xticks(range(len(parameter_labels)), parameter_labels, rotation=45, ha="right")
    plt.xlabel("Parameter Set Index")
    plt.ylabel("Probability")
    plt.title("No Synchronization Probability")
    plt.legend()

    # Plot synchronization only between Alice and Bob probabilities
    plt.subplot(2, 3, 4)
    plt.plot(sync_only_AB_probs, label="Sync AB Only Probability", marker='o')
    plt.xticks(range(len(parameter_labels)), parameter_labels, rotation=45, ha="right")
    plt.xlabel("Parameter Set Index")
    plt.ylabel("Probability")
    plt.title("Synchronization AB Only Probability")
    plt.legend()

    # Plot synchronization among Alice, Bob, and Eve probabilities
    plt.subplot(2, 3, 5)
    plt.plot(sync_ABE_probs, label="Sync ABE Probability", marker='o')
    plt.xticks(range(len(parameter_labels)), parameter_labels, rotation=45, ha="right")
    plt.xlabel("Parameter Set Index")
    plt.ylabel("Probability")
    plt.title("Synchronization ABE Probability")
    plt.legend()

    # Adjust layout and show the plots
    plt.tight_layout()
    plt.show()

# Run simulations for each parameter set and print results
num_simulations = 100  # Increase the number of simulations

results = []
for params in parameter_sets:
    simple_attack_prob, majority_attack_prob, no_sync_prob, sync_only_AB_prob, sync_ABE_prob = run_simulation(*params, num_simulations)
    results.append((simple_attack_prob, majority_attack_prob, no_sync_prob, sync_only_AB_prob, sync_ABE_prob))

print_table(parameter_sets, results)
plot_results(parameter_sets, results)
