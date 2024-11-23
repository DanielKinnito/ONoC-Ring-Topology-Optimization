from heapq import heappop, heappush
from metrics import calculate_path_score

def find_best_path(graph, source, target, wc, wt):
    """Finds the best path using a weighted metric."""
    queue = [(0, source, [])]
    visited = set()
    best_path = None
    best_score = float('inf')

    while queue:
        score, current, path = heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        if current == target:
            path_score = calculate_path_score(graph, path, wc, wt)
            if path_score < best_score:
                best_score = path_score
                best_path = path
            continue

        for neighbor in graph.neighbors(current):
            heappush(queue, (score, neighbor, path))

    return best_path, best_score

def bidirectional_search(graph, source, target, wc, wt):
    """Performs a bidirectional search and selects the optimal path."""
    clockwise_path, clockwise_score = find_best_path(graph, source, target, wc, wt)
    counterclockwise_path, counterclockwise_score = find_best_path(graph, target, source, wc, wt)

    if clockwise_score < counterclockwise_score:
        return clockwise_path, clockwise_score
    else:
        return counterclockwise_path[::-1], counterclockwise_score

def multicast_search(graph, sources, targets, wc, wt):
    """Performs a multicast search and selects the optimal paths."""
    best_paths = []
    best_scores = []

    for source, target in zip(sources, targets):
        best_path, best_score = bidirectional_search(graph, source, target, wc, wt)
        best_paths.append(best_path)
        best_scores.append(best_score)

    return best_paths, best_scores