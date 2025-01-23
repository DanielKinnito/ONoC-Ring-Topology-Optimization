from src.core.topology import create_ring_topology, partition_nodes
from src.core.routing import multicast_search, shortest_path_first
from src.visualization.visualizer import (visualize_topology, 
                                        visualize_metrics_comparison,
                                        create_interactive_visualization,
                                        save_simulation_metrics,
                                        save_node_partition_metrics)
from src.test.test_scenarios import create_test_scenario_1, create_test_scenario_2
import logging
import os
import time
import numpy as np
from collections import defaultdict
from queue import PriorityQueue

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
    handlers=[
        logging.FileHandler('results/simulation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('ONoC_Simulation')

class SimulationEvent:
    """Represents a discrete event in the simulation."""
    def __init__(self, time, event_type, data):
        self.time = time
        self.event_type = event_type
        self.data = data
    
    def __lt__(self, other):
        return self.time < other.time

class SimulationStats:
    """Collects and manages simulation statistics."""
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_time = time.time()
    
    def record_metric(self, metric_name, value):
        self.metrics[metric_name].append(value)
    
    def get_summary(self):
        summary = {}
        for metric, values in self.metrics.items():
            summary[metric] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': min(values),
                'max': max(values)
            }
        return summary

def validate_input_parameters(num_nodes, partition_size, wc, wt, sources, targets):
    """Validates input parameters for the simulation."""
    if num_nodes <= 0:
        raise ValueError("Number of nodes must be positive")
    if partition_size <= 0 or partition_size > num_nodes:
        raise ValueError("Invalid partition size")
    if not (0 <= wc <= 1) or not (0 <= wt <= 1):
        raise ValueError("Weights must be between 0 and 1")
    if not (wc + wt == 1):
        raise ValueError("Weights must sum to 1")
    if not all(0 <= s < num_nodes for s in sources):
        raise ValueError("Invalid source nodes")
    if not all(0 <= t < num_nodes for t in targets):
        raise ValueError("Invalid target nodes")
    logger.info("Input parameters validated successfully")

def setup_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        'results/metrics',
        'results/plots',
        'results/test/metrics',
        'results/test/plots',
        'docs/latex'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    logger.info("Directory setup completed")

def run_discrete_event_simulation(ring, sources, targets, wc, wt):
    """Runs the discrete event simulation."""
    event_queue = PriorityQueue()
    current_time = 0
    stats = SimulationStats()
    
    # Initialize events
    for source in sources:
        event_queue.put(SimulationEvent(current_time, 'packet_generation', {
            'source': source,
            'targets': targets
        }))
    
    # Process events
    while not event_queue.empty():
        event = event_queue.get()
        current_time = event.time
        
        if event.event_type == 'packet_generation':
            # Handle packet generation
            source = event.data['source']
            targets = event.data['targets']
            
            # Run routing algorithms
            paths_tempcon, scores_tempcon = multicast_search(ring, [source], 
                                                           targets, wc, wt)
            paths_spf, scores_spf = shortest_path_first(ring, [source], targets)
            
            # Record metrics
            stats.record_metric('tempcon_congestion', scores_tempcon['congestion'])
            stats.record_metric('tempcon_temperature', scores_tempcon['temperature'])
            stats.record_metric('spf_path_length', len(paths_spf))
            
            # Schedule next packet generation
            next_time = current_time + np.random.exponential(10)  # Mean inter-arrival time
            event_queue.put(SimulationEvent(next_time, 'packet_generation', {
                'source': source,
                'targets': targets
            }))
    
    return stats

def main(num_nodes, partition_size, wc, wt, sources, targets, test_scenario=None, test_name=None):
    """Main simulation function with improved error handling and logging."""
    setup_directories()
    logger.info("Starting simulation with parameters: "
                f"nodes={num_nodes}, partition_size={partition_size}, "
                f"wc={wc}, wt={wt}")
    
    try:
        # Validate input parameters
        validate_input_parameters(num_nodes, partition_size, wc, wt, sources, targets)
        
        # Create topology
        ring = create_ring_topology(num_nodes)
        logger.info("Ring topology created successfully")
        
        # Apply test scenario if provided
        if test_scenario:
            ring = test_scenario(ring)
            logger.info(f"Applied test scenario: {test_scenario.__name__}")
        
        # Partition nodes
        partitions = partition_nodes(ring, partition_size)
        logger.info(f"Network partitioned into {len(partitions)} partitions")
        
        # Run discrete event simulation
        stats = run_discrete_event_simulation(ring, sources, targets, wc, wt)
        logger.info("Discrete event simulation completed")
        
        # Log simulation statistics
        summary = stats.get_summary()
        for metric, values in summary.items():
            logger.info(f"{metric}: {values}")
        
        # Run algorithms for visualization
        paths_tempcon, scores_tempcon = multicast_search(ring, sources, 
                                                       targets, wc, wt)
        paths_spf, scores_spf = shortest_path_first(ring, sources, targets)
        
        # Visualize results
        visualize_topology(ring, paths_tempcon, paths_spf, sources, 
                         targets, partition_size)
        visualize_metrics_comparison(ring, paths_tempcon, paths_spf, wc, wt, test_name)
        create_interactive_visualization(ring, paths_tempcon, paths_spf, sources, targets)
        
        # Save metrics
        save_simulation_metrics(ring, paths_tempcon, paths_spf, wc, wt, test_name)
        save_node_partition_metrics(ring, partitions, test_name)
        
        logger.info("Simulation completed successfully")
        
    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}")
        raise

if __name__ == "__main__":
    sources = [0, 10]
    targets = [5, 15]
    main(20, 5, 0.7, 0.3, sources, targets)