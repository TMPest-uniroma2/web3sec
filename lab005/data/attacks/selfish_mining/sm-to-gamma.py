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
            # Selfish miner trova un blocco
            if state == 0:
                state = 1
                hidden_blocks = 1
            else:
                state += 1
                hidden_blocks += 1
        else:
            # Honest miner trova un blocco
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


def plot_selfish_vs_gamma():
    alphas = [i / 100 for i in range(5, 50)]  # α from 0.05 to 0.49
    gammas = [0.1, 0.3, 0.5, 0.7, 0.9]  # Sybil influence on γ
    rounds = 10000

    plt.figure(figsize=(12, 7))

    for gamma in gammas:
        rewards = [simulate_selfish(a, gamma, rounds) for a in alphas]
        plt.plot(alphas, rewards, label=f'γ = {gamma}', marker='o')

        # Calcola e mostra tipping point
        for a, r in zip(alphas, rewards):
            if r > a:
                plt.plot(a, r, 'x', color='black', markersize=10)
                plt.text(a, r + 0.01, f'{a:.2f}', fontsize=9, ha='center')
                break

    plt.plot(alphas, alphas, label='Baseline (honest)', linestyle='--', color='black')
    plt.xlabel("α (Selfish miner hashrate)")
    plt.ylabel("Reward ratio")
    plt.title("Selfish Mining Reward vs α – Tipping Point per γ (influenza Sybil)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_selfish_vs_gamma()
