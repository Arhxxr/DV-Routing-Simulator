#Arham Shams Sameer
#1002078834

import time
from network import Network

class DVRoutingSimulator:
    
    def __init__(self):
        self.network = Network()
        self.iteration_count = 0
        self.stable_state = False
        self.start_time = 0
        self.end_time = 0
        
    def load_network(self, filename): #loads network topology from a file
        success = self.network.load_from_file(filename)
        if success:
            self.reset_simulation()
        return success
        
    def reset_simulation(self): #resets the simulation state
        self.iteration_count = 0
        self.stable_state = False
        self.start_time = 0
        self.end_time = 0
        
        for node in self.network.nodes.values():
            node.initialize_dv_table(self.network.get_all_node_ids())
    
    def perform_iteration(self): #performs one iteration of the DV routing algorithm
        if self.iteration_count == 0: #starts time measurement if first iteration
            self.start_time = time.time()
        
        self.iteration_count += 1
        any_updates = False
        
        
        current_dvs = {} #for each node, gets its current DV table
        for node_id, node in self.network.nodes.items():
            current_dvs[node_id] = node.dv_table.copy()
        
        for node_id, node in self.network.nodes.items(): #sends DV updates to neighbors
            for neighbor_id in node.get_neighbors(): #for each neighbor
                if self.network.nodes[neighbor_id].update_dv_table(node_id, current_dvs[node_id]): #updates the neighbor's DV table with this node's DV
                    any_updates = True
        
        self.stable_state = not any_updates
        
        if self.stable_state and self.end_time == 0: #records end time if stable state is reached
            self.end_time = time.time()
        
        return not self.stable_state
    
    def run_to_completion(self): #run until stable state
        self.reset_simulation()
        
        while not self.stable_state:
            self.perform_iteration()
            
        return {
            "iterations": self.iteration_count,
            "time": self.end_time - self.start_time
        }
    
    def get_all_dv_tables(self): #gets all current DV tables
        tables = {}
        for node_id, node in self.network.nodes.items():
            tables[node_id] = node.dv_table.copy()
        return tables
    
    def update_link_cost(self, node1, node2, new_cost):
        result = self.network.update_link_cost(node1, node2, new_cost)
        if result: #resets iteration count but keeps the stable state
            self.iteration_count = 0
            self.stable_state = False
            self.start_time = 0
            self.end_time = 0
        return result
    
    def reset_link_cost(self, node1, node2):
        result = self.network.reset_link_cost(node1, node2)
        if result: #resets iteration count but keeps the stable state
            self.iteration_count = 0
            self.stable_state = False
            self.start_time = 0
            self.end_time = 0
        return result
