# ONoC-Ring-Topology-Optimization

This project implements an algorithm for optimizing Optical Network-on-Chip (ONoC) ring topology networks with a congestion-aware heuristic algorithm. The project includes a simulation with visualization capabilities.

## Features

- Create a ring topology with a specified number of nodes.
- Partition nodes for load balancing.
- Perform multicast search to find the best paths from multiple sources to multiple targets.
- Visualize the ring topology with temperature and congestion metrics.
- Highlight the best paths and allow interactive selection of source nodes to visualize specific paths.
- Generate summary tables of path metrics and save them to CSV files.

## Requirements

- Python 3.8+
- NetworkX
- Matplotlib
- Pandas

Install the required packages using:

```sh
pip install -r [requirements.txt](http://_vscodecontentref_/1)
```

## Usage

### Running the Simulation

You can run the simulation using the GUI or directly from the command line.

Using the GUI

1.Run the gui.py script:

```python
python gui.py
```

2.Enter the required parameters in the GUI:
    - Number of Nodes
    - Source Nodes (comma-separated)
    - Target Nodes (comma-separated)
    - Partition Size
    - Weight for Congestion (wc)
    - Weight for Temperature (wt)

3.Click "Run Simulation" to start the simulation. The results will be displayed in the console, and the visualizations will be shown in separate windows.

### Using the Command Line

1.Edit the main.py file to specify the parameters:

```python
if __name__ == "__main__":
    sources = [0, 10]  # Example sources
    targets = [50, 60]  # Example targets
    main(100, 10, 0.6, 0.4, sources, targets)
```

2.Run the main.py script:

```python
python main.py
```

## Visualization

The visualization includes
    - The ring topology with nodes colored based on their temperature.
    - The best paths highlighted in red.
    - Source nodes highlighted in green and target nodes in blue.
    - Interactive zoom functionality.
    - Click functionality to highlight the best path from a selected source node in green.

## Generating Summary Tables

The simulation generates summary tables of path metrics (temperature and congestion) and saves them to CSV files. The summary tables include:
    - Node index
    - Temperature (°C)
    - Congestion (%)
    - Weighted Score

## Project Structure

ONoC-Ring-Topology-Optimization/
├── __pycache__/
├── .gitignore
├── [gui.py](http://_vscodecontentref_/2)
├── LICENSE
├── [main.py](http://_vscodecontentref_/3)
├── [metrics.py](http://_vscodecontentref_/4)
├── [path_metrics_summary_1.csv](http://_vscodecontentref_/5)
├── [path_metrics_summary_2.csv](http://_vscodecontentref_/6)
├── [path_metrics_summary.csv](http://_vscodecontentref_/7)
├── [README.md](http://_vscodecontentref_/8)
├── [requirements.txt](http://_vscodecontentref_/9)
├── [routing.py](http://_vscodecontentref_/10)
├── [topology.py](http://_vscodecontentref_/11)
└── [visualization.py](http://_vscodecontentref_/12)

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
