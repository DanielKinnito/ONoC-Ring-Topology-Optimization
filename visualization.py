import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def visualize_topology(graph, best_path, partition_size):
    """Visualizes the ring topology with temperatures and highlights the best path."""
    pos = nx.circular_layout(graph)
    node_colors = [graph.nodes[n]['temperature'] for n in graph.nodes]

    fig, ax = plt.subplots()
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.coolwarm, node_size=500, ax=ax)

    # Highlight the best path
    edges_in_path = list(zip(best_path[:-1], best_path[1:]))
    nx.draw_networkx_edges(graph, pos, edgelist=edges_in_path, edge_color='red', width=2, ax=ax)

    # Add title and color bar
    plt.title("Ring Topology with Temperature and Best Path Highlighted")
    sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm)
    sm.set_array(node_colors)
    plt.colorbar(sm, ax=ax, label='Temperature (°C)')

    # Set up zoom functionality
    def on_zoom(event):
        scale_factor = 1.1 if event.button == 'up' else 0.9
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
        ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
        ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('scroll_event', on_zoom)
    plt.show()

def visualize_path_metrics(graph, path):
    """Visualizes congestion and temperature metrics for the selected path."""
    congestion = [graph[u][v]['utilization'] for u, v in zip(path[:-1], path[1:])]
    temperature = [graph.nodes[node]['temperature'] for node in path]
    indices = range(len(path))

    plt.figure(figsize=(10, 6))

    # Plot congestion as bars
    plt.bar(indices[:-1], congestion, color='blue', alpha=0.6, label='Congestion (%)')

    # Plot temperature as a line
    plt.plot(indices, temperature, color='red', marker='o', label='Temperature (°C)')

    # Add labels and title
    plt.title("Path Metrics: Congestion and Temperature")
    plt.xlabel("Path Node Index")
    plt.ylabel("Metrics")
    plt.legend()
    plt.grid(True)
    plt.show()

def summarize_path_metrics(graph, path, wc, wt):
    """Generates a summary table of the selected path's metrics."""
    data = {
        'Node': path,
        'Temperature (°C)': [graph.nodes[node]['temperature'] for node in path],
        'Congestion (%)': [graph[u][v]['utilization'] for u, v in zip(path[:-1], path[1:])] + [None],
    }

    # Calculate weighted scores
    data['Weighted Score'] = [
        wc * c + wt * t for c, t in zip(data['Congestion (%)'][:-1], data['Temperature (°C)'])
    ] + [None]
    df = pd.DataFrame(data)

    # Print the table to the console
    print("\nSummary Table for Selected Path:")
    print(df.to_string(index=False))
    return df
