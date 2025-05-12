import networkx as nx
import random
import argparse
import matplotlib.pyplot as plt
from scipy.stats import hypergeom


def simulate_single_eclipse_prob(n_honest, n_sybil, k):
    honest_nodes = [f"H{i}" for i in range(n_honest)]
    sybil_nodes = [f"S{i}" for i in range(n_sybil)]
    all_nodes = honest_nodes + sybil_nodes

    # Nodo vittima onesto scelto a caso
    victim = random.choice(honest_nodes)

    # Se non ci sono abbastanza peer → impossibile
    available_peers = [n for n in all_nodes if n != victim]
    if len(available_peers) < k:
        return False

    # Seleziona k peer casuali per la vittima
    victim_peers = random.sample(available_peers, k)

    # Conta quanti sono Sybil
    sybil_count = sum(1 for p in victim_peers if p in sybil_nodes)

    return sybil_count == k


def batch_mode(n_honest, k, runs, sybil_range):
    results_sim = {}
    results_theory = {}

    N = n_honest + max(sybil_range) - 1  # Escludiamo il nodo vittima

    for n_sybil in sybil_range:
        success_count = 0
        for _ in range(runs):
            if simulate_single_eclipse_prob(n_honest, n_sybil, k):
                success_count += 1
        percent_sim = (success_count / runs) * 100
        results_sim[n_sybil] = percent_sim

        # Probabilità ipergeometrica teorica
        M = n_sybil  # successi nella popolazione
        n = k  # estrazioni
        N_total = n_honest + n_sybil - 1  # totale nodi disponibili (meno il victim)

        if M < k or N_total < k:
            percent_theory = 0
        else:
            percent_theory = hypergeom.pmf(k, N_total, M, n) * 100

        results_theory[n_sybil] = percent_theory

        print(f"Sybil: {n_sybil:>3} → Sim: {percent_sim:.1f}%, Theory: {percent_theory:.2f}%")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(list(results_sim.keys()), list(results_sim.values()), label="Simulazione", marker='o')
    plt.plot(list(results_theory.keys()), list(results_theory.values()), label="Teorica (ipergeom.)", linestyle='--',
             marker='x')
    plt.title("Eclipse Attack – Successo vs Numero di Sybil")
    plt.xlabel("Numero di nodi Sybil")
    plt.ylabel("% Successo Eclipse")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--honest', type=int, default=40, help='Number of honest nodes')
    parser.add_argument('--k', type=int, default=8, help='Connections per node')
    parser.add_argument('--runs', type=int, default=100, help='Simulations per setting')
    parser.add_argument('--sybil_min', type=int, default=0, help='Min sybil count')
    parser.add_argument('--sybil_max', type=int, default=40, help='Max sybil count')
    args = parser.parse_args()

    sybil_range = range(args.sybil_min, args.sybil_max + 1, 2)
    batch_mode(args.honest, args.k, args.runs, sybil_range)
