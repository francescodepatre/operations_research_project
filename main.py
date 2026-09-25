"""
visualize_rcsp.py

Draws the graph of the RCSPP instance and highlights the optimal path.
It does not require AMPL: it recreates the instance and computes the optimum
by enumeration (which is perfectly suitable for small graphs like this one,
used only for visualization).

If you want to draw a path obtained directly from AMPL,
see the draw_graph() function at the bottom: simply pass it the list
of used arcs (x[i,j] > 0.5) instead of the one computed here.
"""

import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Same instance as rcsp.dat
# ---------------------------------------------------------------
edges = {
    (1, 2): 4, (1, 3): 2, (2, 3): 1, (2, 4): 5,
    (3, 4): 8, (3, 5): 10, (4, 5): 2, (4, 6): 6, (5, 6): 3,
}
resource = {1: 0, 2: 3, 3: 2, 4: 4, 5: 2, 6: 0}
source, destination = 1, 6

# Fixed node positions (for a readable and reproducible layout)
pos = {
    1: (0, 0.5),
    2: (1, 1),
    3: (1, 0),
    4: (2, 0.7),
    5: (2, 0),
    6: (3, 0.5),
}


def optimal_path(R):
    """Enumerate all simple paths from source to destination and return the best feasible one."""
    G = nx.DiGraph()
    G.add_weighted_edges_from([(i, j, w) for (i, j), w in edges.items()])

    best_path, best_time = None, float("inf")
    for path in nx.all_simple_paths(G, source, destination):
        time = sum(edges[(path[k], path[k + 1])] for k in range(len(path) - 1))
        resource_usage = sum(resource[n] for n in path)
        if resource_usage <= R and time < best_time:
            best_path, best_time = path, time
    return best_path, best_time


def draw_graph(ax, path, time, R):
    G = nx.DiGraph()
    G.add_weighted_edges_from([(i, j, w) for (i, j), w in edges.items()])

    path_edges = list(zip(path, path[1:])) if path else []

    node_colors = []
    for n in G.nodes():
        if n == source:
            node_colors.append("#2ecc71")       # green = source
        elif n == destination:
            node_colors.append("#e74c3c")       # red = destination
        elif path and n in path:
            node_colors.append("#f1c40f")       # yellow = node on the path
        else:
            node_colors.append("#bdc3c7")       # gray = unused node

    edge_colors = ["#e74c3c" if e in path_edges else "#bdc3c7" for e in G.edges()]
    widths = [3.0 if e in path_edges else 1.0 for e in G.edges()]

    nx.draw_networkx_nodes(
        G, pos, ax=ax, node_color=node_colors,
        node_size=700, edgecolors="black"
    )

    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels={n: f"{n}\n(r={resource[n]})" for n in G.nodes()},
        font_size=8
    )

    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color=edge_colors,
        width=widths,
        arrowsize=15,
        connectionstyle="arc3,rad=0.00"
    )

    nx.draw_networkx_edge_labels(
        G, pos, ax=ax,
        edge_labels={(i, j): w for (i, j), w in edges.items()},
        font_size=7
    )

    resource_usage = sum(resource[n] for n in path) if path else 0

    title = (
        f"R = {R}  ->  optimal time = {time}\n"
        f"path: {'-'.join(map(str, path))}  "
        f"(resource used = {resource_usage})"
    )

    ax.set_title(title, fontsize=10)
    ax.axis("off")


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, R in zip(axes, [8, 9]):
        path, time = optimal_path(R)
        draw_graph(ax, path, time, R)

    fig.suptitle(
        "Shortest Path Problem with Resource Constraint - "
        "Threshold Effect of R",
        fontsize=13
    )

    plt.tight_layout()
    plt.savefig("rcsp_comparison.png", dpi=150)
    print("Saved rcsp_comparison.png")