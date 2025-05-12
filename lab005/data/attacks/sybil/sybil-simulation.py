import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import argparse

from matplotlib.patches import Patch


def simulate_sybil_attack(n_honest, n_sybil, k, delay):
    G = nx.Graph()

    for i in range(n_honest):
        G.add_node(f"H{i}", sybil=False)

    for i in range(n_sybil):
        G.add_node(f"S{i}", sybil=True)

    all_nodes = list(G.nodes)
    for node in all_nodes:
        peers = random.sample([n for n in all_nodes if n != node], k=min(k, len(all_nodes) - 1))
        for peer in peers:
            G.add_edge(node, peer)

    victim = random.choice([n for n in G.nodes if not G.nodes[n]['sybil']])
    victim_peers = list(G.neighbors(victim))
    n_sybil_in_peers = sum(1 for p in victim_peers if G.nodes[p]['sybil'])

    pos = nx.kamada_kawai_layout(G)
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 8))  # wider figure

    for step in range(1, len(victim_peers) + 1):
        ax.clear()
        colors = []
        for node in G:
            if node == victim:
                colors.append("cyan")
            elif node in victim_peers[:step]:
                colors.append("red" if G.nodes[node]['sybil'] else "green")
            elif G.nodes[node]['sybil']:
                colors.append("gray")
            else:
                colors.append("lightblue")

        nx.draw(
            G, pos, node_color=colors, with_labels=True, ax=ax,
            node_size=600, font_size=8, edge_color="#CCCCCC"
        )

        n_sybil_in_step = sum(1 for p in victim_peers[:step] if G.nodes[p]['sybil'])
        percent = (n_sybil_in_step / step * 100) if step else 0
        ax.set_title(f"Step {step}/{len(victim_peers)} – {percent:.1f}% Sybil – Victim: {victim}")

        plt.pause(delay)

    legend_elements = [
        Patch(facecolor='cyan', label='Victim Node'),
        Patch(facecolor='green', label='Honest Peer (Connected)'),
        Patch(facecolor='red', label='Sybil Peer (Connected)'),
        Patch(facecolor='lightblue', label='Honest Node'),
        Patch(facecolor='gray', label='Sybil Node'),
    ]

    ax.legend(handles=legend_elements, loc='upper right')

    plt.ioff()
    plt.show()

    print(f"\n🚨 Simulation complete.")
    print(f"Victim {victim} connected to {len(victim_peers)} peers.")
    print(f"🔴 {n_sybil_in_peers} of them were Sybil nodes ({(n_sybil_in_peers / len(victim_peers)) * 100:.2f}%).")
    print("🧠 Consider using PoW/PoS or identity proofs to limit Sybil attacks.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sybil Attack Simulation")
    parser.add_argument('--honest', type=int, default=50, help='Number of honest nodes')
    parser.add_argument('--sybil', type=int, default=30, help='Number of sybil nodes')
    parser.add_argument('--k', type=int, default=8, help='Max connections per node')
    parser.add_argument('--delay', type=float, default=1.5, help='Step delay (in seconds)')

    args = parser.parse_args()

    simulate_sybil_attack(args.honest, args.sybil, args.k, args.delay)
