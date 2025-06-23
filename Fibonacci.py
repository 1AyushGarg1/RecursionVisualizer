
from graphviz import Digraph
import os


# def fibonacci_frames_full_lifecycle(n):
#   os.makedirs("frames", exist_ok=True)
#   node_counter = 0
#   call_stack = []
#   frames = []
#   graph = Digraph(format="png")
#   node_info = {}  # Maps node_id to (n, state)

#   def save_frame(active_id=None, returned_id=None):
#       frame = Digraph(format="png")
#       for node_id, (label, state) in node_info.items():
#           color = {
#               "active": "blue",
#               "returned": "green",
#               "inactive": "lightgray"
#           }[state]
#           frame.node(node_id, label=label, style="filled", fillcolor=color)
#       for parent_id, child_id in call_stack:
#           frame.edge(parent_id, child_id)
#       frame.render(f"frames/frame_{len(frames):03d}", cleanup=True)
#       frames.append(f"frames/frame_{len(frames):03d}.png")

#   def fib(n, parent_id=None):
#       nonlocal node_counter

#       node_id = f"{node_counter}"
#       node_counter += 1
#       label = f"fib({n})"
#       node_info[node_id] = (label, "active")
#       if parent_id is not None:
#           call_stack.append((parent_id, node_id))

#       save_frame(active_id=node_id)  # Call frame

#       # Base case
#       if n <= 1:
#           node_info[node_id] = (label, "returned")
#           save_frame(returned_id=node_id)  # Return frame
#           node_info[node_id] = (label, "inactive")
#           return n

#       # Recursive case
#       left = fib(n - 1, node_id)
#       right = fib(n - 2, node_id)
#       result = left + right

#       node_info[node_id] = (label + f" = {result}", "returned")
#       save_frame(returned_id=node_id)  # Return frame
#       node_info[node_id] = (label + f" = {result}", "inactive")

#       return result

#   fib(n)
#   print("Frames saved to the 'frames' directory.")

import os
from graphviz import Digraph

def fibonacci_frames_full_lifecycle(n:int,id:str):
    os.makedirs(id, exist_ok=True)
    node_counter = 0
    call_stack = []
    frames = []
    graph = Digraph(format="png")
    node_info = {}  # Maps node_id to (label, state)

    def save_frame(active_id=None, returned_id=None):
        frame = Digraph(format="png")
        for node_id, (label, state) in node_info.items():
            color = {
                "active": "blue",
                "returned": "green",
                "inactive": "lightgray"
            }[state]
            frame.node(node_id, label=label, style="filled", fillcolor=color)
        for parent_id, child_id in call_stack:
            frame.edge(parent_id, child_id)
        frame.render(f"{id}/frame_{len(frames):03d}", cleanup=True)
        frames.append(f"{id}/frame_{len(frames):03d}.png")

    def fib(n, parent_id=None):
        nonlocal node_counter

        node_id = f"{node_counter}"
        node_counter += 1
        label = f"fibonacci({n})"
        node_info[node_id] = (label, "active")
        if parent_id is not None:
            call_stack.append((parent_id, node_id))

        save_frame(active_id=node_id)  # Call frame

        # Base case
        if n <= 1:
            result = n
            node_info[node_id] = (f"fibonacci({n}) = {result}", "returned")
            save_frame(returned_id=node_id)  # Return frame
            node_info[node_id] = (f"fibonacci({n}) = {result}", "inactive")
            return result

        # Recursive case
        left = fib(n - 1, node_id)
        right = fib(n - 2, node_id)
        result = left + right

        node_info[node_id] = (f"fibonacci({n}) = {result}", "returned")
        save_frame(returned_id=node_id)  # Return frame
        node_info[node_id] = (f"fibonacci({n}) = {result}", "inactive")

        return result

    fib(n)
    print(f"Frames saved to the {id} directory.")
