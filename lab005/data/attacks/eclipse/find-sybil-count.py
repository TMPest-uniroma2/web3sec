import random
from tqdm import trange


def simulate_single_eclipse_prob(n_honest, n_sybil, k):
    honest_nodes = [f"H{i}" for i in range(n_honest)]
    sybil_nodes = [f"S{i}" for i in range(n_sybil)]
    all_nodes = honest_nodes + sybil_nodes

    victim = random.choice(honest_nodes)
    available_peers = [n for n in all_nodes if n != victim]

    if len(available_peers) < k:
        return False

    victim_peers = random.sample(available_peers, k)
    sybil_count = sum(1 for p in victim_peers if p in sybil_nodes)

    return sybil_count == k


def find_sybil_threshold(n_honest=40, k=8, runs=300, threshold=99.0):
    n_sybil = 0
    while True:
        success_count = 0
        for _ in range(runs):
            if simulate_single_eclipse_prob(n_honest, n_sybil, k):
                success_count += 1

        success_rate = (success_count / runs) * 100
        print(f"Sybil: {n_sybil:<3} → Success rate: {success_rate:.1f}%")

        if success_rate >= threshold:
            print(f"\n[+] Found: {n_sybil} Sybil nodes needed for ≥ {threshold}% success")
            break

        n_sybil += 1
        if n_sybil > 3 * n_honest:
            print("[-] No threshold reached (check model)")
            break


if __name__ == "__main__":
    find_sybil_threshold(n_honest=40, k=8, runs=500, threshold=99.0)
