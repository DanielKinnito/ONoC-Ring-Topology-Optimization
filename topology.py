import networkx as nx
import random

def create_ring_topology(num_nodes):
    """Creates a ring topology with the given number of nodes."""
    ring = nx.cycle_graph(num_nodes)
    for node in ring.nodes:
        ring.nodes[node]['temperature'] = random.uniform(25, 50)  # Initial temperature in °C
        ring.nodes[node]['congestion'] = random.uniform(10, 80)  # Initial congestion in %
    for u, v in ring.edges:
        ring[u][v]['utilization'] = random.uniform(10, 80)  # Link utilization in %
    return ring

def partition_nodes(graph, partition_size):
    """Partitions the nodes into groups of the given size."""
    nodes = list(graph.nodes)
    partitions = [nodes[i:i + partition_size] for i in range(0, len(nodes), partition_size)]
    return partitions
