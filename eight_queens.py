import random
import numpy as np
import matplotlib.pyplot as plt

def calculate_attacks(queens):
    """Calculate the number of attacking queen pairs."""
    n = len(queens)
    attacks = 0
    for i in range(n):
        for j in range(i+1, n):
            if queens[i] == queens[j] or abs(queens[i] - queens[j]) == abs(i - j):
                attacks += 1
    return attacks
    
def generate_random_board():
    """Generate a random configuration for 8-queens."""
    return [random.randint(0, 7) for _ in range(8)]

def hill_climbing_first_choice():
    """First-choice hill climbing for the 8-queens problem."""
    board = generate_random_board()
    while True:
        current_attacks = calculate_attacks(board)
        if current_attacks == 0:
            return board, 0
        neighbors = [list(board) for _ in range(8)]
        for i in range(8):
            neighbors[i][i] = random.randint(0, 7)
        next_board = random.choice(neighbors)
        next_attacks = calculate_attacks(next_board)
        if next_attacks < current_attacks:
            board = next_board
        else:
            return board, current_attacks

def steepest_ascent_hill_climbing():
    """Steepest ascent hill climbing for the 8-queens problem."""
    board = generate_random_board()
    while True:
        current_attacks = calculate_attacks(board)
        if current_attacks == 0:
            return board, 0
        neighbors = [list(board) for _ in range(64)]
        for i in range(8):
            for j in range(8):
                if board[i] != j:
                    new_board = list(board)
                    new_board[i] = j
                    neighbors.append(new_board)
        next_board = min(neighbors, key=calculate_attacks)
        next_attacks = calculate_attacks(next_board)
        if next_attacks < current_attacks:
            board = next_board
        else:
            return board, current_attacks

def simulated_annealing():
    """Simulated annealing for the 8-queens problem."""
    board = generate_random_board()
    current_attacks = calculate_attacks(board)
    T = 100
    while T > 0.01:
        if current_attacks == 0:
            return board, 0
        new_board = list(board)
        i = random.randint(0, 7)
        new_board[i] = random.randint(0, 7)
        new_attacks = calculate_attacks(new_board)
        if (new_attacks < current_attacks
                or random.uniform(0, 1)
                < np.exp((current_attacks - new_attacks) / T)):
            board = new_board
            current_attacks = new_attacks
        T *= 0.99
    return board, current_attacks

def random_restart_hill_climbing():
    """Hill climbing with random restart for the 8-queens problem."""
    for _ in range(100):
        board, cost = steepest_ascent_hill_climbing()
        if cost == 0:
            return board, 0
    return None, None

methods = {
    'First-Choice Hill Climbing': hill_climbing_first_choice,
    'Steepest-Ascent Hill Climbing': steepest_ascent_hill_climbing,
    'Simulated Annealing': simulated_annealing,
    'Random Restart Hill Climbing': random_restart_hill_climbing
}

results = {method: {'cost': [], 'solved': 0} for method in methods}

for method_name, method in methods.items():
    for _ in range(100):  # 100 test cases
        board, cost = method()
        if cost == 0:
            results[method_name]['solved'] += 1
        results[method_name]['cost'].append(cost)

for method_name, data in results.items():
    plt.plot(data['cost'], label=f'{method_name} (Solved: {data["solved"]}%)')

plt.xlabel('Test Case')
plt.ylabel('Solution Cost')
plt.legend()
plt.show()

for method_name, data in results.items():
    success_rate = data['solved']
    print(f"{method_name}: {success_rate}% problems solved.")
