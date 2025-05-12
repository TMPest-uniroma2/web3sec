import networkx as nx
import random
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, timedelta
import pandas as pd
from matplotlib.patches import Patch

from lib.eclipse import detect_eclipse
from lib.selfish import detect_selfish
from lib.sybil import detect_sybil


def generate_ip(sybil=False):
    return f"192.168.1.{random.randint(1, 254)}" if sybil else f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def generate_asn(sybil=False):
    return "AS64512" if sybil else f"AS{random.randint(10000, 65000)}"


def generate_geo(sybil=False):
    return "IT-Rome" if sybil else random.choice(["US-New York", "DE-Berlin", "FR-Paris", "JP-Tokyo", "BR-Sao Paulo"])


def generate_timestamp(base_time, sybil=False):
    return base_time + timedelta(seconds=random.randint(0, 60 if sybil else 3600))


def create_p2p_network(total_nodes=100, sybil_nodes=10, selfish_nodes=5, eclipse_nodes=5):
    G = nx.Graph()
    base_time = datetime.now()

    for i in range(total_nodes):
        node_id = f"Node_{i}"
        is_sybil = i < sybil_nodes
        is_selfish = sybil_nodes <= i < sybil_nodes + selfish_nodes
        is_eclipse = sybil_nodes + selfish_nodes <= i < sybil_nodes + selfish_nodes + eclipse_nodes

        G.add_node(node_id,
                   ip=generate_ip(is_sybil),
                   asn=generate_asn(is_sybil),
                   geo=generate_geo(is_sybil),
                   timestamp=generate_timestamp(base_time, is_sybil),
                   known_sybil=is_sybil,
                   known_selfish=is_selfish,
                   known_eclipse=is_eclipse)

    nodes = list(G.nodes())
    for node in nodes:
        if G.nodes[node].get("known_eclipse", False):
            # Connect only to Sybil nodes (force eclipse condition)
            sybil_peers = [n for n, d in G.nodes(data=True) if d.get("known_sybil", False)]
            peers = random.sample(sybil_peers, k=min(3, len(sybil_peers)))  # fully sybil-connected
            for peer in peers:
                G.add_edge(node, peer)
        else:
            peers = random.sample([n for n in nodes if n != node], k=random.randint(2, 5))
            for peer in peers:
                G.add_edge(node, peer)
    return G

# =========================================
# TODO: Exercise - How to detect attacks?
# =========================================
def detect_sybil_nodes(G):
    return detect_sybil(graph=G)


def detect_eclipse_nodes(G):
    return detect_eclipse(graph=G)


def detect_selfish_nodes(G):
    return detect_selfish(graph=G)


def evaluate_detection(G, detected, label):
    key = f"known_{label}"
    tp = sum(1 for n in detected if G.nodes[n].get(key, False))
    fp = len(detected) - tp
    fn = sum(1 for n, d in G.nodes(data=True) if d.get(key, False) and n not in detected)
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print(f"\n📊 Detection Evaluation – {label.upper()}")
    print(f"  TP = {tp}, FP = {fp}, FN = {fn}")
    print(f"  Precision = {precision:.2f}, Recall = {recall:.2f}, F1 = {f1:.2f}")


def plot_detection(G, detected_nodes, label):
    ground_key = f"known_{label}"
    pos = nx.kamada_kawai_layout(G)
    node_colors = []

    for n in G.nodes():
        is_known = G.nodes[n].get(ground_key, False)
        is_detected = n in detected_nodes

        if is_known and is_detected:
            node_colors.append('red')  # TP
        elif is_known and not is_detected:
            node_colors.append('purple')  # FN
        elif not is_known and is_detected:
            node_colors.append('orange')  # FP
        else:
            node_colors.append('green')  # TN

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=8)
    legend_elements = [
        Patch(facecolor='red', label=f'{label} – Detected (TP)'),
        Patch(facecolor='purple', label=f'{label} – Missed (FN)'),
        Patch(facecolor='orange', label=f'{label} – False Positive (FP)'),
        Patch(facecolor='green', label='Normal (TN)')
    ]
    plt.legend(handles=legend_elements, loc='best')
    plt.title(f"Rete P2P – Detection: {label.upper()}")
    plt.show()


def build_detection_df(G, label, detected_nodes):
    key = f"known_{label}"
    rows = []
    for n, d in G.nodes(data=True):
        known = d.get(key, False)
        detected = n in detected_nodes
        if known and detected:
            status = "TP"
        elif known and not detected:
            status = "FN"
        elif not known and detected:
            status = "FP"
        else:
            status = "TN"
        rows.append({
            "node": n,
            "ip": d['ip'],
            "asn": d['asn'],
            "geo": d['geo'],
            "timestamp": d['timestamp'],
            "ground_truth": known,
            "detected": detected,
            "result": status,
            "type": label
        })
    return pd.DataFrame(rows)


def main():
    G = create_p2p_network()

    results = []

    for label, detect_fn in {
        "sybil": detect_sybil_nodes,
        "eclipse": detect_eclipse_nodes,
        "selfish": detect_selfish_nodes
    }.items():
        detected = detect_fn(G)
        evaluate_detection(G, detected, label)
        plot_detection(G, detected, label)
        results.append(build_detection_df(G, label, detected))

    df_all = pd.concat(results)
    print("\n📋 Full Detection Summary:")
    print(df_all.sort_values(by=["type", "result"]))

    # Optional: export
    # df_all.to_csv("p2p_detection_summary.csv", index=False)


if __name__ == "__main__":
    main()
