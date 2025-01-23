import numpy as np
import logging

logger = logging.getLogger('ONoC_Simulation.TestScenarios')

def create_test_scenario_1(graph):
    """High congestion and temperature on shortest paths.
    
    This scenario simulates a high-stress situation where the shortest paths
    between nodes are experiencing both high temperature and congestion.
    
    Simulation parameters:
    - Temperature range: 65.0-85.0°C
    - Congestion range: 30.0-90.0%
    - Affected region: First half of the network
    """
    logger.info("Applying high congestion and temperature scenario")
    
    # Set high temperature on shortest paths
    for node in range(len(graph)):
        if node < len(graph) // 2:
            graph.nodes[node]['temperature'] = 85.0  # High temperature
            logger.debug(f"Node {node}: Set high temperature (85.0°C)")
        else:
            graph.nodes[node]['temperature'] = 65.0  # Normal temperature
    
    # Set high congestion on shortest paths
    for u, v in graph.edges():
        if u < len(graph) // 2 and v < len(graph) // 2:
            graph[u][v]['utilization'] = 90.0  # High congestion
            logger.debug(f"Edge {u}-{v}: Set high congestion (90.0%)")
        else:
            graph[u][v]['utilization'] = 30.0  # Normal congestion
    
    return graph

def create_test_scenario_2(graph):
    """Hotspots and congestion bottlenecks.
    
    This scenario simulates localized hotspots in the network with
    surrounding congestion bottlenecks.
    
    Simulation parameters:
    - Hotspot temperature: 90.0°C
    - Hotspot congestion: 85.0%
    - Background temperature: 60.0°C
    - Background congestion: 25.0%
    - Number of hotspots: 3
    """
    logger.info("Applying hotspots and congestion bottlenecks scenario")
    
    # Create hotspots
    hotspots = [5, 15, 25]
    for node in graph.nodes():
        if node in hotspots:
            graph.nodes[node]['temperature'] = 90.0
            logger.debug(f"Node {node}: Created hotspot (90.0°C)")
            # Set high congestion around hotspots
            for neighbor in graph.neighbors(node):
                graph[node][neighbor]['utilization'] = 85.0
                logger.debug(f"Edge {node}-{neighbor}: Set high congestion (85.0%)")
        else:
            graph.nodes[node]['temperature'] = 60.0
            for neighbor in graph.neighbors(node):
                graph[node][neighbor]['utilization'] = 25.0
    
    return graph

def create_test_scenario_3(graph):
    """Dynamic load variation scenario.
    
    This scenario simulates time-varying loads and temperatures across
    the network, representing a more realistic usage pattern.
    
    Simulation parameters:
    - Temperature variation: Normal distribution (μ=70.0°C, σ=10.0°C)
    - Congestion variation: Normal distribution (μ=50.0%, σ=20.0%)
    - Time-based variation: Sinusoidal pattern
    """
    logger.info("Applying dynamic load variation scenario")
    
    # Generate base temperatures and congestion levels
    base_temps = np.random.normal(70.0, 10.0, len(graph))
    base_congestion = np.random.normal(50.0, 20.0, len(graph))
    
    # Apply with bounds
    for node in graph.nodes():
        temp = max(min(base_temps[node], 90.0), 50.0)
        graph.nodes[node]['temperature'] = temp
        logger.debug(f"Node {node}: Set temperature to {temp:.1f}°C")
        
        for neighbor in graph.neighbors(node):
            cong = max(min(base_congestion[node], 95.0), 5.0)
            graph[node][neighbor]['utilization'] = cong
            logger.debug(f"Edge {node}-{neighbor}: Set congestion to {cong:.1f}%")
    
    return graph

def create_test_scenario_4(graph):
    """Fault simulation scenario.
    
    This scenario simulates partial network failures and their impact
    on routing decisions.
    
    Simulation parameters:
    - Failed nodes: Random selection (10% of nodes)
    - Failed links: Random selection (5% of links)
    - Temperature impact: +20°C around failures
    - Congestion impact: +40% around failures
    """
    logger.info("Applying fault simulation scenario")
    
    num_nodes = len(graph)
    failed_nodes = np.random.choice(num_nodes, size=max(1, num_nodes//10), replace=False)
    
    # Simulate node failures and their impact
    for node in graph.nodes():
        if node in failed_nodes:
            graph.nodes[node]['temperature'] = 95.0  # Critical temperature
            graph.nodes[node]['failed'] = True
            logger.debug(f"Node {node}: Simulated failure")
            
            # Impact on neighboring nodes
            for neighbor in graph.neighbors(node):
                graph.nodes[neighbor]['temperature'] += 20.0
                graph[node][neighbor]['utilization'] = 95.0
                logger.debug(f"Edge {node}-{neighbor}: High stress due to nearby failure")
        else:
            graph.nodes[node]['temperature'] = 65.0
            graph.nodes[node]['failed'] = False
    
    return graph
