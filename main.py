from topology import create_ring_topology, partition_nodes
from routing import bidirectional_search
from visualization import visualize_topology, visualize_path_metrics, summarize_path_metrics

def main():
    # Parameters
    num_nodes = 200
    partition_size = 10
    wc, wt = 0.6, 0.4  # Weights for congestion and temperature

    # Create the ring topology
    ring = create_ring_topology(num_nodes)

    # Partition nodes (optional step, can be used for load balancing)
    partitions = partition_nodes(ring, partition_size)

    # Define source and target nodes
    source, target = 0, 50

    # Perform bidirectional search to find the best path
    best_path, best_score = bidirectional_search(ring, source, target, wc, wt)

    # Display results in the console
    print("Best Path:", best_path)
    print("Best Score:", best_score)

    # Visualize the ring topology with the best path highlighted
    visualize_topology(ring, best_path)

    # Visualize the path metrics (congestion and temperature)
    visualize_path_metrics(ring, best_path)

    # Generate a summary table for the selected path and save it to a CSV file
    summary_df = summarize_path_metrics(ring, best_path, wc, wt)
    summary_df.to_csv("path_metrics_summary.csv", index=False)
    print("Summary saved as path_metrics_summary.csv")

if __name__ == "__main__":
    main()
