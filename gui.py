import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import time
from dv_routing import DVRoutingSimulator

class DVRoutingGUI:
    
    def __init__(self, master):
        self.master = master
        self.simulator = DVRoutingSimulator()
        
        self.create_widgets()
        self.create_layout()
        
        self.current_file = "sample_network.txt"
        self.load_network(self.current_file)
    
    def create_widgets(self):
        self.control_frame = ttk.LabelFrame(self.master, text="Control Panel") #controls frame widgets
        
        #file selections
        self.file_frame = ttk.Frame(self.control_frame) 
        self.file_label = ttk.Label(self.file_frame, text="Network File:")
        self.file_entry = ttk.Entry(self.file_frame, width=30)
        self.file_button = ttk.Button(self.file_frame, text="Browse...", command=self.browse_file)
        self.load_button = ttk.Button(self.file_frame, text="Load Network", command=self.load_network_from_entry)
        
        #simulation controls
        self.sim_frame = ttk.Frame(self.control_frame) 
        self.step_button = ttk.Button(self.sim_frame, text="Step", command=self.step_simulation)
        self.auto_button = ttk.Button(self.sim_frame, text="Run to Completion", command=self.run_to_completion)
        self.reset_button = ttk.Button(self.sim_frame, text="Reset", command=self.reset_simulation)
        
        #status display
        self.status_frame = ttk.Frame(self.control_frame) 
        self.status_label = ttk.Label(self.status_frame, text="Status:")
        self.status_var = tk.StringVar(value="Not started")
        self.status_display = ttk.Label(self.status_frame, textvariable=self.status_var)
        
        self.iter_label = ttk.Label(self.status_frame, text="Iterations:")
        self.iter_var = tk.StringVar(value="0")
        self.iter_display = ttk.Label(self.status_frame, textvariable=self.iter_var)
        
        self.time_label = ttk.Label(self.status_frame, text="Time:")
        self.time_var = tk.StringVar(value="0.0 sec")
        self.time_display = ttk.Label(self.status_frame, textvariable=self.time_var)
        
        #link modification
        self.link_frame = ttk.LabelFrame(self.control_frame, text="Link Management") 
        
        self.link_node1_label = ttk.Label(self.link_frame, text="Node 1:")
        self.link_node1_var = tk.StringVar()
        self.link_node1_combo = ttk.Combobox(self.link_frame, textvariable=self.link_node1_var, state="readonly", width=5)
        
        self.link_node2_label = ttk.Label(self.link_frame, text="Node 2:")
        self.link_node2_var = tk.StringVar()
        self.link_node2_combo = ttk.Combobox(self.link_frame, textvariable=self.link_node2_var, state="readonly", width=5)
        
        self.link_cost_label = ttk.Label(self.link_frame, text="New Cost:")
        self.link_cost_var = tk.StringVar(value="16")
        self.link_cost_entry = ttk.Entry(self.link_frame, textvariable=self.link_cost_var, width=5)
        
        self.update_link_button = ttk.Button(self.link_frame, text="Update Link", command=self.update_link)
        self.reset_link_button = ttk.Button(self.link_frame, text="Reset Link", command=self.reset_link)
        
        #results frame
        self.results_frame = ttk.LabelFrame(self.master, text="Network Visualization") 
        
        #table display
        self.tables_frame = ttk.Frame(self.results_frame) 
        
        #log display
        self.log_frame = ttk.LabelFrame(self.master, text="Simulation Log") 
        self.log_text = scrolledtext.ScrolledText(self.log_frame, width=80, height=10)
        self.log_text.config(state=tk.DISABLED)
        

        self.table_frames = {} #table frame container
        self.table_labels = {} #table label container
        
    def create_layout(self):
        #main layout
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5) 
        self.results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        #controls frame layout
        self.file_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5) 
        self.file_label.pack(side=tk.LEFT, padx=5)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.file_button.pack(side=tk.LEFT, padx=5)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.sim_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.step_button.pack(side=tk.LEFT, padx=5)
        self.auto_button.pack(side=tk.LEFT, padx=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.status_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.status_label.pack(side=tk.LEFT, padx=5)
        self.status_display.pack(side=tk.LEFT, padx=5)
        self.iter_label.pack(side=tk.LEFT, padx=5)
        self.iter_display.pack(side=tk.LEFT, padx=5)
        self.time_label.pack(side=tk.LEFT, padx=5)
        self.time_display.pack(side=tk.LEFT, padx=5)
        
        self.link_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.link_node1_label.grid(row=0, column=0, padx=5, pady=5)
        self.link_node1_combo.grid(row=0, column=1, padx=5, pady=5)
        self.link_node2_label.grid(row=0, column=2, padx=5, pady=5)
        self.link_node2_combo.grid(row=0, column=3, padx=5, pady=5)
        self.link_cost_label.grid(row=0, column=4, padx=5, pady=5)
        self.link_cost_entry.grid(row=0, column=5, padx=5, pady=5)
        self.update_link_button.grid(row=0, column=6, padx=5, pady=5)
        self.reset_link_button.grid(row=0, column=7, padx=5, pady=5)
        
        self.tables_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def browse_file(self): #browses for a network topology file
        filename = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
    
    def load_network_from_entry(self): #loads network from the file specified in the entry field
        filename = self.file_entry.get().strip()
        if filename:
            self.load_network(filename)
        else:
            messagebox.showwarning("Warning", "Please select a network file.")
    
    def load_network(self, filename): #loads network from specified file
        success = self.simulator.load_network(filename)
        if success:
            self.current_file = filename
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            self.log(f"Network loaded from {filename}")
            
            #updates node lists for link management
            node_ids = self.simulator.network.get_all_node_ids()
            self.link_node1_combo['values'] = node_ids
            self.link_node2_combo['values'] = node_ids
            
            if node_ids:
                self.link_node1_var.set(node_ids[0])
                self.link_node2_var.set(node_ids[1] if len(node_ids) > 1 else node_ids[0])
            
            self.update_tables_display()
            self.status_var.set("Ready")
            self.iter_var.set("0")
            self.time_var.set("0.0 sec")
        else:
            messagebox.showerror("Error", f"Failed to load network from {filename}")
    
    def update_tables_display(self):
        for widget in self.tables_frame.winfo_children():#clears previous tables
            widget.destroy()

        node_ids = self.simulator.network.get_all_node_ids() #gets all node IDs
        if not node_ids:
            return
        
        dv_tables = self.simulator.get_all_dv_tables() #gets current DV tables
        

        num_nodes = len(node_ids) #calculates grid layout
        cols = min(3, num_nodes) #max 3 tables per row
        rows = (num_nodes + cols - 1) // cols #ceil division
        
        for i, node_id in enumerate(node_ids): #create and lays out tables
            row = i // cols
            col = i % cols
            
            #creates frame for the node's table
            node_frame = ttk.LabelFrame(self.tables_frame, text=f"Node {node_id} DV Table")
            node_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            #creates table headers
            ttk.Label(node_frame, text="Dest").grid(row=0, column=0, padx=5, pady=2)
            ttk.Label(node_frame, text="Cost").grid(row=0, column=1, padx=5, pady=2)
            ttk.Label(node_frame, text="Next Hop").grid(row=0, column=2, padx=5, pady=2)
            
            #fills table with data
            for j, dest_id in enumerate(sorted(dv_tables[node_id].keys())):
                cost, next_hop = dv_tables[node_id][dest_id]
                cost_str = str(cost) if cost < 16 else "∞"
                next_hop_str = str(next_hop) if next_hop is not None else "-"
                
                ttk.Label(node_frame, text=str(dest_id)).grid(row=j+1, column=0, padx=5, pady=2)
                ttk.Label(node_frame, text=cost_str).grid(row=j+1, column=1, padx=5, pady=2)
                ttk.Label(node_frame, text=next_hop_str).grid(row=j+1, column=2, padx=5, pady=2)
        
        #grid configuration to properly resize
        for i in range(rows):
            self.tables_frame.grid_rowconfigure(i, weight=1)
        for i in range(cols):
            self.tables_frame.grid_columnconfigure(i, weight=1)
    
    def step_simulation(self): #run one step of the simulation
        changes = self.simulator.perform_iteration()
        
        self.update_tables_display()
        self.iter_var.set(str(self.simulator.iteration_count))
        
        if self.simulator.start_time > 0 and self.simulator.end_time > 0:
            self.time_var.set(f"{self.simulator.end_time - self.simulator.start_time:.4f} sec")
        
        if self.simulator.stable_state:
            self.status_var.set("Stable State Reached")
            self.log(f"Stable state reached after {self.simulator.iteration_count} iterations")
            self.log(f"Total time: {self.simulator.end_time - self.simulator.start_time:.4f} seconds")
            messagebox.showinfo("Simulation Complete", "Stable state reached!")
        else:
            self.status_var.set("Running")
            self.log(f"Iteration {self.simulator.iteration_count} completed")
    
    def run_to_completion(self): #run until stable state
        result = self.simulator.run_to_completion()
        
        self.update_tables_display()
        self.iter_var.set(str(result["iterations"]))
        self.time_var.set(f"{result['time']:.4f} sec")
        self.status_var.set("Stable State Reached")
        
        self.log(f"Stable state reached after {result['iterations']} iterations")
        self.log(f"Total time: {result['time']:.4f} seconds")
        
        messagebox.showinfo("Simulation Complete", 
                           f"Stable state reached after {result['iterations']} iterations!\n"
                           f"Total time: {result['time']:.4f} seconds")
    
    def reset_simulation(self):
        self.simulator.reset_simulation()
        
        self.update_tables_display()
        self.iter_var.set("0")
        self.time_var.set("0.0 sec")
        self.status_var.set("Ready")
        
        self.log("Simulation reset")
    
    def update_link(self): #updates the cost of a link
        try:
            node1 = int(self.link_node1_var.get())
            node2 = int(self.link_node2_var.get())
            cost = int(self.link_cost_var.get())
            
            if node1 == node2:
                messagebox.showwarning("Invalid Link", "Cannot update link to self")
                return
            
            result = self.simulator.update_link_cost(node1, node2, cost)
            if result:
                self.update_tables_display()
                self.iter_var.set("0")
                self.time_var.set("0.0 sec")
                self.status_var.set("Ready - Link Updated")
                
                cost_str = str(cost) if cost < 16 else "∞"
                self.log(f"Link between Node {node1} and Node {node2} updated to cost {cost_str}")
            else:
                messagebox.showwarning("Warning", f"No link exists between Node {node1} and Node {node2}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid node IDs and cost")
    
    def reset_link(self): #resets the cost of a link to original value
        try:
            node1 = int(self.link_node1_var.get())
            node2 = int(self.link_node2_var.get())
            
            if node1 == node2:
                messagebox.showwarning("Invalid Link", "Cannot reset link to self")
                return
            
            result = self.simulator.reset_link_cost(node1, node2)
            if result:
                self.update_tables_display()
                self.iter_var.set("0")
                self.time_var.set("0.0 sec")
                self.status_var.set("Ready - Link Reset")

                for link in self.simulator.network.links: #gets the current cost after reset
                    if (link.node1 == node1 and link.node2 == node2) or \
                       (link.node1 == node2 and link.node2 == node1):
                        self.log(f"Link between Node {node1} and Node {node2} reset to original cost {link.cost}")
                        break
            else:
                messagebox.showwarning("Warning", f"No link exists between Node {node1} and Node {node2}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid node IDs")
    
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
