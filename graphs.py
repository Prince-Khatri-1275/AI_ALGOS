import pandas as pd
class Node:
    id = 0
    look_up_table = pd.DataFrame(columns=["id", "name", "node"])
    def __init__(self, name):
        self.name = name
        self.id = Node.next_id()
        Node.join(self)
    
    @classmethod
    def join(cls, node):
        cls.look_up_table.loc[len(cls.look_up_table)] = [node.id, node.name, node]

    @classmethod
    def next_id(cls):
        cls.id += 1
        return cls.id
    
    def __repr__(self):
        return f"Node_{self.name}"

Node("m")
Node("k")

print(Node.look_up_table)