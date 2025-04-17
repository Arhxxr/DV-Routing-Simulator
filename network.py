#Arham Shams Sameer
#1002078834

class Link: #ink between two nodes with a cost
    def __init__(self, node1, node2, cost):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost
        self.original_cost = cost #original cost is stored for link repair
    
    def __str__(self):
        return f"{self.node1} <--{self.cost}--> {self.node2}"
    
    def get_other_node(self, node): #returns the node on the other side of the link
        if node == self.node1:
            return self.node2
        elif node == self.node2:
            return self.node1
        return None 

class Node: #node/router in the network
    def __init__(self, node_id):
        self.node_id = node_id
        self.links = []
        self.dv_table = {} #maps destination nodes to (cost, next_hop)
        self.updated = False #tracks if the DV table was updated in current run
    
    def __str__(self):
        return f"Node {self.node_id}"
    
    def add_link(self, link): 
        if link not in self.links:
            self.links.append(link)
    
    def get_neighbors(self): #returns all neighboring nodes
        neighbors = []
        for link in self.links:
            neighbor = link.get_other_node(self.node_id)
            neighbors.append(neighbor)
        return neighbors
    
    def get_link_to(self, node_id): #gets link to a specific neighbor node
        for link in self.links:
            if link.node1 == node_id or link.node2 == node_id:
                return link
        return None
    
    def get_link_cost(self, node_id): #gets link cost
        link = self.get_link_to(node_id)
        if link:
            return link.cost
        return float('inf')
    
    def initialize_dv_table(self, all_nodes):
        self.dv_table = {self.node_id: (0, self.node_id)} #sets distance to self as 0
        
        for neighbor in self.get_neighbors(): #sets distance to direct neighbors based on link costs
            cost = self.get_link_cost(neighbor)
            self.dv_table[neighbor] = (cost, neighbor)
        
        for node in all_nodes: #sets distance to non-neighbors as infinity | 16 = infinity
            if node != self.node_id and node not in self.dv_table:
                self.dv_table[node] = (16, None)
    
    def update_dv_table(self, neighbor_id, neighbor_dv):
        self.updated = False

        link_cost = self.get_link_cost(neighbor_id) #cost to reach the neighbor
        
        if link_cost >= 16: #if neighbor can't be reached, ignore (since 16 = infinity)
            return False
        
        for dest_id, (dest_cost, _) in neighbor_dv.items():
            new_cost = link_cost + dest_cost
            
            if new_cost >= 16:
                new_cost = 16 #sets new cost to 16 if it exceeds

            if dest_id not in self.dv_table or new_cost < self.dv_table[dest_id][0]: #if there's a route to this destination or new route is better
                self.dv_table[dest_id] = (new_cost, neighbor_id)
                self.updated = True
        
        return self.updated

class Network:
    def __init__(self):
        self.nodes = {}  #map of node_id to node objects
        self.links = []  #list of Link objects
    
    def load_from_file(self, filename):
        self.nodes = {}
        self.links = []
        
        try:
            with open(filename, 'r') as file:
                for line in file:
                    if not line.strip() or line.strip().startswith('#'):
                        continue
                    
                    parts = line.strip().split()
                    if len(parts) == 3:
                        try:
                            node1 = int(parts[0])
                            node2 = int(parts[1])
                            cost = int(parts[2])
                            
                            #creates nodes if they don't exist
                            if node1 not in self.nodes:
                                self.nodes[node1] = Node(node1)
                            if node2 not in self.nodes:
                                self.nodes[node2] = Node(node2)
                            
                            #creates and adds the link
                            link = Link(node1, node2, cost)
                            self.links.append(link)
                            self.nodes[node1].add_link(link)
                            self.nodes[node2].add_link(link)
                        except ValueError:
                            print(f"Invalid line format: {line}")
                    else:
                        print(f"Invalid line format: {line}")

            for node in self.nodes.values():
                node.initialize_dv_table(self.nodes.keys())
            
            return True
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return False
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def get_all_node_ids(self):
        return sorted(list(self.nodes.keys()))
    
    def update_link_cost(self, node1, node2, new_cost):
        for link in self.links:
            if (link.node1 == node1 and link.node2 == node2) or \
               (link.node1 == node2 and link.node2 == node1):
                link.cost = new_cost
                
                for node in self.nodes.values(): #reinitializes DV tables after link cost change
                    node.initialize_dv_table(self.nodes.keys())
                return True
        return False
    
    def reset_link_cost(self, node1, node2):
        for link in self.links:
            if (link.node1 == node1 and link.node2 == node2) or \
               (link.node1 == node2 and link.node2 == node1):
                link.cost = link.original_cost
                
                for node in self.nodes.values():
                    node.initialize_dv_table(self.nodes.keys())
                return True
        return False
