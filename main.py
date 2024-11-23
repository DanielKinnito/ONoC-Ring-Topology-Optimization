from topology import create_ring_topology, partition_nodes
from routing import bidirectional_search, multicast_search
from visualization import visualize_topology, visualize_path_metrics, summarize_path_metrics

def main(num_nodes, partition_size, wc, wt, sources, targets):
    # Create the ring topology
    ring = create_ring_topology(num_nodes)

    # Partition nodes (optional step, can be used for load balancing)
    partitions = partition_nodes(ring, partition_size)

    # Perform multicast search to find the best paths
    best_paths, best_scores = multicast_search(ring, sources, targets, wc, wt)

    # Display results in the console
    for i, (path, score) in enumerate(zip(best_paths, best_scores)):
        print(f"Best Path {i+1}:", path)
        print(f"Best Score {i+1}:", score)

    # Visualize the ring topology with the best paths highlighted
    visualize_topology(ring, best_paths, sources, targets, partition_size)

    # Visualize the path metrics (congestion and temperature)
    for path in best_paths:
        visualize_path_metrics(ring, path)

    # Generate a summary table for the selected paths and save it to a CSV file
    for i, path in enumerate(best_paths):
        summary_df = summarize_path_metrics(ring, path, wc, wt)
        summary_df.to_csv(f"path_metrics_summary_{i+1}.csv", index=False)
        print(f"Summary saved as path_metrics_summary_{i+1}.csv")

if __name__ == "__main__":
    sources = [0, 10]  # Example sources
    targets = [50, 60]  # Example targets
    main(100, 10, 0.6, 0.4, sources, targets)