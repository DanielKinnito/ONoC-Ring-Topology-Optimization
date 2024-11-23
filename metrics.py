def calculate_temperature(delta_lambda, alpha=1.86e-4, lambda_o=1550, T_o=25):
    """Calculates the temperature from the resonant wavelength shift."""
    delta_T = delta_lambda / (lambda_o * alpha)
    return T_o + delta_T

def calculate_congestion(graph, path):
    """Calculates the total congestion for a given path."""
    return sum(graph[u][v]['utilization'] for u, v in zip(path[:-1], path[1:]))

def calculate_path_score(graph, path, wc, wt):
    """Calculates the weighted score for a given path."""
    congestion = calculate_congestion(graph, path)
    temperature = sum(graph.nodes[node]['temperature'] for node in path)
    return wc * congestion + wt * temperature
