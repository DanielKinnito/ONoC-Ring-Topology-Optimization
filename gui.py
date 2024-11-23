import tkinter as tk
from tkinter import ttk, messagebox
from main import main  # Import the main simulation function

def run_simulation():
    """Run the simulation with the specified parameters."""
    try:
        num_nodes = int(entry_nodes.get())
        source_node = int(entry_source.get())
        target_node = int(entry_target.get())
        partition_size = int(entry_partition.get())
        wc = float(entry_wc.get())
        wt = float(entry_wt.get())

        if source_node >= num_nodes or target_node >= num_nodes:
            messagebox.showerror("Error", "Source or Target node is out of range!")
            return

        # Run the simulation with specified parameters
        main(num_nodes, partition_size, wc, wt, source_node, target_node)

        # Show success message
        messagebox.showinfo("Success", "Simulation completed successfully! Check the graphs and CSV file.")
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

ttk.Label(frame, text="Source Node:").grid(column=0, row=1, sticky=tk.W)
entry_source = ttk.Entry(frame, width=20)
entry_source.grid(column=1, row=1)
entry_source.insert(0, "0")

ttk.Label(frame, text="Target Node:").grid(column=0, row=2, sticky=tk.W)
entry_target = ttk.Entry(frame, width=20)
entry_target.grid(column=1, row=2)
entry_target.insert(0, "50")

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
