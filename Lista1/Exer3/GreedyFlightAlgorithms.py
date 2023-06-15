# As operações seguem a sintaxe (origem, destino, custo)
operations = [
("a", "b", 1), 
("a", "c", 9), 
("a", "d", 4), 
("b", "c", 7), 
("b", "e", 6), 
("b", "f", 1), 
("c", "f", 7), 
("d", "f", 4),
("d", "g", 5), 
("e", "h", 9), 
("f", "h", 4), 
("g", "h", 1)
]

class Node:
    def __init__(self, city, parent, cost):
        self.city = city
        self.parent = parent
        self.cost = cost

    def GenerateNewNodes(self):
        newNodes = []

        for i in range(12):   
            if self.city == operations[i][0]:         
                newNode = Node(operations[i][1], self, operations[i][2])
                newNodes.append(newNode)

        return newNodes
        
    def __eq__(self, __value: object) -> bool:
        return self.city == __value.city
    
def GreedyBestFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(initial_city, None, 0))

    while len(openNodes) > 0:
        print("Nodos abertos: ", [n.city for n in openNodes])
        print("Nodos fechados: ", [n.city for n in closedNodes])
        openNodes.sort(key=lambda x: x.cost)
        node = openNodes.pop(0)
        closedNodes.append(node)

        if node.city == goal_city:
            return node

        for childNode in node.GenerateNewNodes():
            validNodes = []
            if childNode not in openNodes and childNode not in closedNodes:
                validNodes.append(childNode)            
            openNodes = validNodes + openNodes

    return None

def DepthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(initial_city, None, 0))

    while len(openNodes) > 0:
        node = openNodes.pop(0)
        closedNodes.append(node)

        if node.city == goal_city:
            return node

        for childNode in node.GenerateNewNodes():
            validNodes = []
            if childNode not in openNodes and childNode not in closedNodes:
                validNodes.append(childNode)            
            openNodes = validNodes + openNodes

    return None

def BreadthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(initial_city, None, 0))

    while len(openNodes) > 0:
        node = openNodes.pop(0)
        closedNodes.append(node)

        if node.city == goal_city:
            return node

        for childNode in node.GenerateNewNodes():
            if childNode not in openNodes and childNode not in closedNodes:
                openNodes.append(childNode)

    return None

def SearchCostCalculator(result):
    aux = result
    cost = 0
    while aux.parent is not None:
        cost += aux.cost
        aux = aux.parent
    return cost

def PrintSearchPath(result):
    if result is not None:
        aux = result
        path = []
        path.append(aux)

        while aux.parent is not None:
            aux = aux.parent
            path.append(aux)

        path.reverse()

        for node in path:
            print(node.city)
    else:
        print("Não foi possível encontrar uma solução.")

# Estado inicial e objetivo
initial_city = "a"
goal_city = "h"

# Chama a busca em profundidade
gbfs = GreedyBestFirstSearch()
dfs = DepthFirstSearch()
bfs = BreadthFirstSearch()

# Imprime o caminho encontrado
print("Caminho encontrado pela busca em profundidade:")
PrintSearchPath(gbfs)
print("Custo da busca gulosa pela melhor escolhar: ", SearchCostCalculator(gbfs))
print("Custo da busca em profundidade:", SearchCostCalculator(dfs))
print("Custo da busca em largura:", SearchCostCalculator(bfs))
