#Arham Shams Sameer
#1002078834

import tkinter as tk
from gui import DVRoutingGUI
def main():
    root = tk.Tk() #initializes the GUI
    root.title("Distance Vector Routing Simulator")
    root.geometry("1200x800")
    
    app = DVRoutingGUI(root) #creates the GUI
    
    root.mainloop() #begins the main loop
if __name__ == "__main__":
    main()