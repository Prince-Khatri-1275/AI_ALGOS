class Stack:
    def __init__(self, elements:list|None=None):
        self.frontier = []
        if elements:
            self.add(elements)
    
    def isEmpty(self):
        return len(self.frontier)==0
    
    def add(self, elements):
        if isinstance(elements, list):
            self.frontier.extend(elements)
        else:
            self.frontier.append(elements)

    def pop(self):
        return self.frontier.pop()

class Queue:
    def __init__(self, elements:list|None=None):
        self.frontier = []
        if elements:
            self.add(elements)
    
    def isEmpty(self):
        return len(self.frontier)==0
    
    def add(self, elements):
        if isinstance(elements, list):
            [self.frontier.insert(0, element) for element in elements]
        else:
            self.frontier.insert(0, elements)

    def pop(self):
        return self.frontier.pop(0)
    