from utils import Stack

def dfs(start, goal, graph):
    # Step 1: Put start into stack
    # Step 2: If the stack is empty then return None
    #         Fetch this element as currentNode
    # Step 3: If the currentNode is goal then return the path
    # Step 4: Else Add the children of the currentNode to the stack
    # Step 5: Repeat the Steps 2 to 4 until an result is found
    
    # Step 1:-
    stack = Stack([start])

    # Step 5:-
    while True:
        # Step 2:-
        if stack.isEmpty():
            return None
        currentNode = stack.pop() # Step 2.5
        
        # Step 3:-
        if currentNode is goal:
            return currentNode.get_path()
        
        # Step 4:-
        for child in currentNode.get_childs():
            stack.add(child)
