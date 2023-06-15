# As operações seguem a sintaxe (id, origem, destino)
operations = [
("1", "a", "b"), 
("2", "a", "b"), 
("3", "a", "d"), 
("4", "b", "e"), 
("5", "b", "f"), 
("6", "c", "g"), 
("7", "c", "h"),
("8", "c", "i"), 
("9", "d", "j"), 
("10", "e", "k"), 
("11", "e", "l"), 
("12", "g", "m"), 
("13", "j", "n"), 
("14", "j", "o"),
("15", "k", "f"), 
("16", "l", "h"), 
("17", "m", "d"), 
("18", "o", "a"), 
("19", "n", "b")
]

class Node:
    def __init__(self, city, parent):
        self.city = city;
        self.parent = parent

    def GenerateNewNodes(self):
        newNodes = []

        for i in range(19):   
            if self.city == operations[i][1]:         
                newNode = Node(operations[i][2], self)
                newNodes.append(newNode)

        return newNodes
        
    def __eq__(self, __value: object) -> bool:
        return self.city == __value.city
    
# Depth-First Search
def DepthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(initial_city, None))

    while len(openNodes) > 0:
        print("Nodos abertos: ", [n.city for n in openNodes])
        print("Nodos fechados: ", [n.city for n in closedNodes])
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

    openNodes.append(Node(initial_city, None))

    while len(openNodes) > 0:
        print("Nodos abertos: ", [n.city for n in openNodes])
        print("Nodos fechados: ", [n.city for n in closedNodes])
        node = openNodes.pop(0)
        closedNodes.append(node)

        if node.city == goal_city:
            return node

        for childNode in node.GenerateNewNodes():
            if childNode not in openNodes and childNode not in closedNodes:
                openNodes.append(childNode)

    return None

# Estado inicial e objetivo
initial_city = "a"
goal_city = "j"

# Chama a busca em profundidade
result = BreadthFirstSearch()

print("Etapas:")

# Imprime o caminho encontrado
if result is not None:
    path = []
    path.append(result)

    while result.parent is not None:
        result = result.parent
        path.append(result)

    path.reverse()

    for node in path:
        print(node.city)
else:
    print("Não foi possível encontrar uma solução.")
