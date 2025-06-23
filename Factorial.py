import os
from graphviz import Digraph

def factorial_frames_full_lifecycle(n:int,id:str):
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

    def fact(n, parent_id=None):
        nonlocal node_counter

        node_id = f"{node_counter}"
        node_counter += 1
        label = f"factorial({n})"
        node_info[node_id] = (label, "active")
        if parent_id is not None:
            call_stack.append((parent_id, node_id))

        save_frame(active_id=node_id)  # Call frame

        # Base case
        if n <= 1:
            result = 1
            node_info[node_id] = (f"factorial({n}) = {result}", "returned")
            save_frame(returned_id=node_id)  # Return frame
            node_info[node_id] = (f"factorial({n}) = {result}", "inactive")
            return result

        # Recursive case
        left = fact(n - 1, node_id)
        result = left*n

        node_info[node_id] = (f"factorial({n}) = {result}", "returned")
        save_frame(returned_id=node_id)  # Return frame
        node_info[node_id] = (f"factorial({n}) = {result}", "inactive")

        return result

    fact(n)
    print(f"Frames saved to the {id} directory.")