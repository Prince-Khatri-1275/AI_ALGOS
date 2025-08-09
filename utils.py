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
    

def sqrt(num, k_iters=10000):
    best_approximation = num/2
    for i in range(k_iters):
        best_approximation = (best_approximation+num/best_approximation)/2
        print(f'Iteration:- {i} | best_approximation:- {best_approximation:.6f}')
        
    
    return best_approximation

def herons_sqrt(num, epsilon=1e-7, limit_i=1000):
    best_approximation = num/2
    i = 0
    while True:
        best_approximation = (best_approximation+num/best_approximation)/2
        print(f'Iteration:- {i} | best_approximation:- {best_approximation:.6f}')
        i += 1
        print(abs(best_approximation*best_approximation-num))
        if abs(best_approximation**2-num)<=epsilon or i>=limit_i:
            break
    
    return best_approximation


num = 1282659000000005548451518481545102
root = sqrt(num) # 1282659000000005548451518481545102
print(root)
print(root*root-num)