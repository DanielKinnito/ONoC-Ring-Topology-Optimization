from topology import create_ring_topology, partition_nodes
from routing import bidirectional_search, multicast_search, shortest_path_first
from visualization import visualize_topology, visualize_path_metrics, summarize_path_metrics

def main(num_nodes, partition_size, wc, wt, sources, targets):
    # Create the ring topology
    ring = create_ring_topology(num_nodes)

    # Partition nodes (optional step, can be used for load balancing)
    partitions = partition_nodes(ring, partition_size)

    # Perform multicast search to find the best paths using TempCon-RingCast
    best_paths_tempcon, best_scores_tempcon = multicast_search(ring, sources, targets, wc, wt)

    # Perform shortest path first search to find the best paths
    best_paths_spf, best_scores_spf = shortest_path_first(ring, sources, targets)

    # Display results in the console for TempCon-RingCast
    print("TempCon-RingCast Results:")
    for i, (path, score) in enumerate(zip(best_paths_tempcon, best_scores_tempcon)):
        print(f"Best Path {i+1}:", path)
        print(f"Best Score {i+1}:", score)

    # Display results in the console for Shortest Path First
    print("Shortest Path First Results:")
    for i, (path, score) in enumerate(zip(best_paths_spf, best_scores_spf)):
        print(f"Best Path {i+1}:", path)
        print(f"Best Score {i+1}:", score)

    # Visualize the ring topology with the best paths highlighted for both algorithms
    visualize_topology(ring, best_paths_tempcon, best_paths_spf, sources, targets, partition_size)

    # Visualize the path metrics (congestion and temperature) for TempCon-RingCast
    for path in best_paths_tempcon:
        visualize_path_metrics(ring, path, "TempCon-RingCast")

    # Visualize the path metrics (congestion and temperature) for Shortest Path First
    for path in best_paths_spf:
        visualize_path_metrics(ring, path, "Shortest Path First")

    # Generate a summary table for the selected paths and save it to a CSV file for TempCon-RingCast
    for i, path in enumerate(best_paths_tempcon):
        summary_df = summarize_path_metrics(ring, path, wc, wt)
        summary_df.to_csv(f"path_metrics_summary_tempcon_{i+1}.csv", index=False)
        print(f"Summary saved as path_metrics_summary_tempcon_{i+1}.csv")

    # Generate a summary table for the selected paths and save it to a CSV file for Shortest Path First
    for i, path in enumerate(best_paths_spf):
        summary_df = summarize_path_metrics(ring, path, wc, wt)
        summary_df.to_csv(f"path_metrics_summary_spf_{i+1}.csv", index=False)
        print(f"Summary saved as path_metrics_summary_spf_{i+1}.csv")

if __name__ == "__main__":
    sources = [4, 37]  # Example sources
    targets = [5, 16]  # Example targets
    main(100, 10, 0.6, 0.4, sources, targets)