# Distance Vector Routing Simulator
A network project developed as part of the CSE4344: Computer Network Organization Course
## Running the simulator
- Download or clone the repo.
- Extract all the files into one folder.
- Open terminal/command-prompt at that folder and run: `python main.py`
## GUI Elements:
1. Network Visualization/DV tables display. (Pictures in Initializing the node section)

2. Control Panel (File Selection, Step button, Run to Completion button, Reset button).

3. Status Display (Running, Stable State, Iteration Count, Time taken to reach stability).

4. Link Management (Interface to select two nodes and modify their link cost, Button to reset link to original cost).

5. Simulation Log (Text area showing simulation events and results, Timestamps for actions and state changes).

![image](https://github.com/user-attachments/assets/f1b887d2-05e0-4422-bf17-af65fcf56eb1)
___

# Functionality

## File Input
- Located in `network.py` within the `Network.load_from_file()` method.
- Each line contains three numbers: node1 node2 cost.
- Each line represents a bidirectional link between two nodes with an associated cost.
- 1 2 7 means there is a link between Node 1 and Node 2 with a cost of 7.
- Maximum number of nodes: 6 | Maximum links per node: 4.

The file is read line by line, and for each valid entry, the nodes and cost are extracted, if the nodes don’t exist yet, they’re created, a Link is added to both, and once everything’s loaded, all nodes initialize their DV tables.

## Node Initialization

- When loaded, it displays the DV tables for all the nodes in the file.
- Located in network.py within the Node.initialize_dv_table() method.
- Each node's DV table is a dictionary mapping destinations to (cost, next_hop).
- Initial values are set according to: 
  1) Cost to self = 0 (next hop is self).
  2) Cost to direct neighbors = direct link cost (next hop is the neighbor).
  3) Cost to all other nodes = infinity (represented as 16, next hop is None).
 
## Sending DV to Neighbors

- Located in dv_routing.py within the DVRoutingSimulator.perform_iteration() method.
- First collects the current DV tables from all nodes.
- Then for each node, it sends its DV table to all its neighbors by calling the neighbor's update method.

![image](https://github.com/user-attachments/assets/5025123c-7fc6-4657-8cf1-f9f19a26ac3e)
- This simulates the simultaneous exchange of DV tables among all nodes in the network.

## Updating Own DV

-	Located in dv_routing.py within the DVRoutingSimulator.perform_iteration() method.
- The simulator tracks whether any updates occurred during the current iteration/run.
- Before each iteration, sets any_updates = False.
- During the iteration, if any node updates its table, sets any_updates = True.
- After processing all nodes, checks if any_updates is still False.
- If no updates occurred, sets self.stable_state = True. 
- The stable state is displayed to the user.

## Adjucting Link Cost

- **Network level:** Located in network.py within the Network.update_link_cost() and Network.reset_link_cost() methods.
- **Simulator level:** Located in dv_routing.py within the DVRoutingSimulator.update_link_cost() and DVRoutingSimulator.reset_link_cost() methods.
- **GUI level:** Located in gui.py within the DVRoutingGUI.update_link() and DVRoutingGUI.reset_link() methods.

- ## Link Failure Simulation </br>
  Setting a link cost to 16 (infinity) simulates a link failure. Once updated, all nodes reinitialize their DV tables, and the algorithm runs from this new state until it stabilizes, with nodes finding alternative paths around the failed link.

- ## Link Repair Simulation </br>
  Resetting a link to its original cost simulates a repair, with the original cost stored in the Link object at creation. After resetting, all nodes reinitialize their DV tables, the algorithm runs until stability, and nodes may revert to previously optimal paths that use the repaired link.



