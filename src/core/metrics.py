import numpy as np
from collections import defaultdict
import logging

logger = logging.getLogger('ONoC_Simulation.Metrics')

class NetworkMetrics:
    """Manages network performance metrics collection and analysis."""
    def __init__(self):
        self.metrics = defaultdict(list)
        self.path_history = []
        self.temperature_history = []
        self.congestion_history = []
    
    def record_path(self, path, time):
        """Records path metrics at a given simulation time."""
        self.path_history.append((time, path))
    
    def record_temperature(self, node, temperature, time):
        """Records node temperature at a given simulation time."""
        self.temperature_history.append((time, node, temperature))
    
    def record_congestion(self, edge, congestion, time):
        """Records edge congestion at a given simulation time."""
        self.congestion_history.append((time, edge, congestion))
    
    def get_average_metrics(self):
        """Calculates average metrics over the simulation period."""
        avg_metrics = {}
        
        # Calculate average path length
        if self.path_history:
            path_lengths = [len(path) for _, path in self.path_history]
            avg_metrics['avg_path_length'] = np.mean(path_lengths)
            avg_metrics['std_path_length'] = np.std(path_lengths)
        
        # Calculate average temperature
        if self.temperature_history:
            temperatures = [temp for _, _, temp in self.temperature_history]
            avg_metrics['avg_temperature'] = np.mean(temperatures)
            avg_metrics['std_temperature'] = np.std(temperatures)
        
        # Calculate average congestion
        if self.congestion_history:
            congestions = [cong for _, _, cong in self.congestion_history]
            avg_metrics['avg_congestion'] = np.mean(congestions)
            avg_metrics['std_congestion'] = np.std(congestions)
        
        return avg_metrics

def calculate_temperature(delta_lambda, alpha=1.86e-4, lambda_o=1550, T_o=25):
    """Calculates the temperature from the resonant wavelength shift."""
    if not isinstance(delta_lambda, (int, float)) or delta_lambda < 0:
        raise ValueError("Invalid wavelength shift value")
    
    delta_T = delta_lambda / (lambda_o * alpha)
    return T_o + delta_T

def calculate_congestion(graph, path):
    """Calculates the total congestion for a given path."""
    if len(path) < 2:
        return 0
        
    congestion = 0
    for u, v in zip(path[:-1], path[1:]):
        if not graph.has_edge(u, v):
            raise ValueError(f"Invalid path: no edge between {u} and {v}")
        congestion += graph[u][v]['utilization']
    
    return congestion

def calculate_path_score(graph, path, wc, wt):
    """Calculates the weighted score for a given path."""
    if not (0 <= wc <= 1 and 0 <= wt <= 1 and abs(wc + wt - 1) < 1e-6):
        raise ValueError("Weights must be between 0 and 1 and sum to 1")
        
    congestion = calculate_congestion(graph, path)
    temperature = sum(graph.nodes[node]['temperature'] for node in path)
    
    # Normalize scores
    avg_congestion = np.mean([graph[u][v]['utilization'] for u, v in graph.edges])
    avg_temperature = np.mean([graph.nodes[n]['temperature'] for n in graph.nodes])
    
    normalized_congestion = congestion / (len(path) * avg_congestion) if avg_congestion > 0 else 0
    normalized_temperature = temperature / (len(path) * avg_temperature) if avg_temperature > 0 else 0
    
    return wc * normalized_congestion + wt * normalized_temperature

def calculate_network_performance(graph, paths, time_window=None):
    """Calculates comprehensive network performance metrics."""
    performance_metrics = {
        'throughput': 0,
        'latency': 0,
        'energy_efficiency': 0,
        'reliability': 0
    }
    
    try:
        # Calculate throughput (packets per time unit)
        total_packets = sum(len(path) - 1 for path in paths)
        if time_window:
            performance_metrics['throughput'] = total_packets / time_window
        
        # Calculate average latency
        total_latency = sum(len(path) for path in paths)
        performance_metrics['latency'] = total_latency / len(paths) if paths else 0
        
        # Calculate energy efficiency (simplified model)
        total_hops = sum(len(path) - 1 for path in paths)
        performance_metrics['energy_efficiency'] = total_packets / (total_hops + 1)
        
        # Calculate reliability (based on temperature and congestion)
        max_temp = max(data['temperature'] for _, data in graph.nodes(data=True))
        max_cong = max(data['utilization'] for _, _, data in graph.edges(data=True))
        performance_metrics['reliability'] = 1 - (max_temp/100 + max_cong)/2
        
        logger.debug(f"Performance metrics calculated: {performance_metrics}")
        return performance_metrics
        
    except Exception as e:
        logger.error(f"Error calculating network performance: {str(e)}")
        raise
