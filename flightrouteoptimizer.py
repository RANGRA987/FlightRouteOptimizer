import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import json
import os

DATA_FILE = "flight_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(graph, file, indent=4)
graph = load_data()

def dijkstra(graph, start, end):
    if start not in graph or end not in graph:
        return [], "No Path"
    pq = []
    heapq.heappush(pq, (0, start))
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {node: None for node in graph}

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_node == end:
            break
        for neighbor, weight in graph[curr_node].items():
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = curr_node
                heapq.heappush(pq, (distance, neighbor))
    path = []
    node = end
    while node is not None:
        path.insert(0, node)
        node = parent[node]
    return path, distances[end] if distances[end] != float('inf') else "No Path"

def add_airport():
    airport = airport_entry.get().strip()
    if airport:
        if airport in graph:
            messagebox.showwarning("Duplicate Airport", "Airport already exists.")
        else:
            graph[airport] = {}
            save_data()
            messagebox.showinfo("Success", f"Airport '{airport}' added.")
    else:
        messagebox.showwarning("Invalid Input", "Please enter a valid airport name.")

def add_route():
    src = source_entry.get().strip()
    dest = dest_entry.get().strip()
    try:
        weight = int(distance_entry.get().strip())
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid distance (in km).")
        return
    if not src or not dest:
        messagebox.showwarning("Invalid Input", "Please enter valid airport names.")
        return
    if src not in graph or dest not in graph:
        messagebox.showerror("Error", "Both airports must exist.")
        return
    graph[src][dest] = weight
    graph[dest][src] = weight  
    save_data() 
    messagebox.showinfo("Success", f"Route added between {src} and {dest} with distance {weight} km.")

def find_shortest_path():
    start = source_entry.get().strip()
    end = dest_entry.get().strip()
    if not start or not end:
        messagebox.showwarning("Input Error", "Please enter both source and destination.")
        return
    if start == end:
        messagebox.showinfo("Invalid Input", "Source and destination cannot be the same.")
        return
    if start not in graph or end not in graph:
        messagebox.showerror("Error", "Invalid airport selection")
        return
    path, distance = dijkstra(graph, start, end)

    if distance == "No Path":
        result_label.config(text="No available route")
    else:
        result_label.config(text=f"Shortest Path: {' -> '.join(path)}\nDistance: {distance} km")
    draw_graph(path)

def draw_graph(path):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    pos = nx.circular_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(7, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    if len(path) > 1:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.show()

root = tk.Tk()
root.title("Flight Route Optimizer")
root.geometry("600x600")

tk.Label(root, text="Add Airport").pack()
airport_entry = tk.Entry(root)
airport_entry.pack()
tk.Button(root, text="Add Airport", command=add_airport).pack()

tk.Label(root, text="Enter Source Airport").pack()
source_entry = tk.Entry(root)
source_entry.pack()

tk.Label(root, text="Enter Destination Airport").pack()
dest_entry = tk.Entry(root)
dest_entry.pack()

tk.Label(root, text="Enter Distance (in km)").pack()
distance_entry = tk.Entry(root)
distance_entry.pack()

tk.Button(root, text="Add Route", command=add_route).pack()
tk.Button(root, text="Find Shortest Path", command=find_shortest_path).pack()

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()
root.mainloop()