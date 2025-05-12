import random
import matplotlib.pyplot as plt


def simulate_selfish(alpha, gamma, rounds=10000):
    state = 0
    selfish_blocks = 0
    honest_blocks = 0
    hidden_blocks = 0

    for _ in range(rounds):
        r = random.random()

        if r < alpha:
            if state == 0:
                state = 1
                hidden_blocks = 1
            else:
                state += 1
                hidden_blocks += 1
        else:
            if state == 0:
                honest_blocks += 1
            elif state == 1:
                if random.random() < gamma:
                    selfish_blocks += 1
                else:
                    honest_blocks += 1
                state = 0
                hidden_blocks = 0
            else:
                selfish_blocks += hidden_blocks
                state = 0
                hidden_blocks = 0

    total = selfish_blocks + honest_blocks
    return selfish_blocks / total if total else 0


def plot_selfish_mining_curve(gamma=0.5, rounds=10000):
    alphas = [i / 100 for i in range(5, 50)]
    selfish_ratios = []
    honest_line = []

    for alpha in alphas:
        ratio = simulate_selfish(alpha, gamma, rounds)
        selfish_ratios.append(ratio)
        honest_line.append(alpha)

    plt.figure(figsize=(10, 6))
    plt.plot(alphas, selfish_ratios, label='Selfish Mining Reward', marker='o')
    plt.plot(alphas, honest_line, label='Honest Miner Reward (baseline)', linestyle='--')
    plt.xlabel("α (Selfish miner hashrate)")
    plt.ylabel("Reward ratio")
    plt.title(f"Selfish Mining vs Honest Mining – γ = {gamma}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_selfish_mining_curve(gamma=0.5, rounds=10000)
