import tkinter as tk
from tkinter import ttk, messagebox
from main import main  # Import the main simulation function

def run_simulation():
    """Run the simulation with the specified parameters."""
    try:
        num_nodes = int(entry_nodes.get())
        sources = list(map(int, entry_sources.get().split(',')))
        targets = list(map(int, entry_targets.get().split(',')))
        partition_size = int(entry_partition.get())
        wc = float(entry_wc.get())
        wt = float(entry_wt.get())

        if any(source >= num_nodes for source in sources) or any(target >= num_nodes for target in targets):
            messagebox.showerror("Error", "Source or Target node is out of range!")
            return

        # Run the simulation with specified parameters
        main(num_nodes, partition_size, wc, wt, sources, targets)

        # Show success message
        messagebox.showinfo("Success", "Simulation completed successfully! Check the graphs and CSV files.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for all parameters.")

# Create the main GUI window
root = tk.Tk()
root.title("Network Optimization Simulation")

# Create input fields and labels
frame = ttk.Frame(root, padding="10")
frame.grid()

ttk.Label(frame, text="Number of Nodes:").grid(column=0, row=0, sticky=tk.W)
entry_nodes = ttk.Entry(frame, width=20)
entry_nodes.grid(column=1, row=0)
entry_nodes.insert(0, "200")

ttk.Label(frame, text="Source Nodes (comma-separated):").grid(column=0, row=1, sticky=tk.W)
entry_sources = ttk.Entry(frame, width=20)
entry_sources.grid(column=1, row=1)
entry_sources.insert(0, "0,10")

ttk.Label(frame, text="Target Nodes (comma-separated):").grid(column=0, row=2, sticky=tk.W)
entry_targets = ttk.Entry(frame, width=20)
entry_targets.grid(column=1, row=2)
entry_targets.insert(0, "50,60")

ttk.Label(frame, text="Partition Size:").grid(column=0, row=3, sticky=tk.W)
entry_partition = ttk.Entry(frame, width=20)
entry_partition.grid(column=1, row=3)
entry_partition.insert(0, "10")

ttk.Label(frame, text="Weight for Congestion (wc):").grid(column=0, row=4, sticky=tk.W)
entry_wc = ttk.Entry(frame, width=20)
entry_wc.grid(column=1, row=4)
entry_wc.insert(0, "0.6")

ttk.Label(frame, text="Weight for Temperature (wt):").grid(column=0, row=5, sticky=tk.W)
entry_wt = ttk.Entry(frame, width=20)
entry_wt.grid(column=1, row=5)
entry_wt.insert(0, "0.4")

# Create the Run button
run_button = ttk.Button(frame, text="Run Simulation", command=run_simulation)
run_button.grid(column=0, row=6, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()
