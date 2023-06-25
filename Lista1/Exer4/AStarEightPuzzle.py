from copy import deepcopy

# Problema do Quebra-Cabeça de 8
# 0 foi usado para representar o espaço vazio

class Node:
    def __init__(self, parent, state, cost):
        self.parent = parent
        self.state = state
        self.cost = cost

    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(str(self.state))

    def GenerateNewNodes(self):
        newNodes = []

        emptyIndex = GetIndex(self.state, 0)
        row = emptyIndex[0]
        col = emptyIndex[1]
        
        # Movimento para cima
        if row > 0:
            newState = deepcopy(self.state)
            newState[row][col], newState[row - 1][col] = newState[row - 1][col], newState[row][col]
            newNodes.append(Node(self, newState, self.cost + 1))

        # Movimento para baixo
        if row < 2:
            newState = deepcopy(self.state)
            newState[row][col], newState[row + 1][col] = newState[row + 1][col], newState[row][col]
            newNodes.append(Node(self, newState, self.cost + 1))

        # Movimento para esquerda
        if col > 0:
            newState = deepcopy(self.state)
            newState[row][col], newState[row][col - 1] = newState[row][col - 1], newState[row][col]
            newNodes.append(Node(self, newState, self.cost + 1))

        # Movimento para direita
        if col < 2:
            newState = deepcopy(self.state)
            newState[row][col], newState[row][col + 1] = newState[row][col + 1], newState[row][col]
            newNodes.append(Node(self, newState, self.cost + 1))

        return newNodes
    
# Procura por um valor em uma tabela e retorna o índice  
def GetIndex(state, value):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == value:
                return (i, j)

# Função heurística
def h(state):
    distance = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            value = state[i][j]
            goalIndex = GetIndex(goalState, value)
            distance += abs(i - goalIndex[0]) + abs(j - goalIndex[1])
    return distance
    
aStarVisited = []
# Busca A*
def AStarSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, initialState, h(initialState)))

    while len(openNodes) > 0:
        currentNode = openNodes.pop(0)
        aStarVisited.append(currentNode)
        closedNodes.append(currentNode)

        if currentNode.state == goalState:
            return currentNode

        newNodes = currentNode.GenerateNewNodes()

        for node in newNodes:
            if node not in closedNodes:
                openNodes.append(node)

        openNodes.sort(key=lambda node: node.cost + h(node.state))
        
        print("Nodos abertos: ", [n.state for n in openNodes])
        print("Nodos fechados: ", [n.state for n in closedNodes])

    return None

# Imprime o caminho encontrado
def PrintSearchPath(result):
    aux = result
    path = []
    path.append(aux)

    while aux.parent is not None:
        aux = aux.parent
        path.append(aux)

    path.reverse()

    for node in path:
        print(node.state[0])
        print(node.state[1])
        print(node.state[2])
        print()
    print()

# Método para desenhar a árvore de busca
def DrawSearchTree(visited_nodes):
    node_map = {}
    for node in visited_nodes:
        if node.parent is not None:
            if node.parent not in node_map:
                node_map[node.parent] = []
            node_map[node.parent].append(node)

    RecursiveDraw(node_map, visited_nodes[0], "")

def RecursiveDraw(node_map, node, prefix):
    if prefix:
        print(prefix[:-1] + "└── ", node.state)
    else:
        print(node.state)

    if node in node_map:
        children = node_map[node]
        for i, child in enumerate(children):
            if i == len(children) - 1:
                RecursiveDraw(node_map, child, prefix + "    ")
            else:
                RecursiveDraw(node_map, child, prefix + "│   ")

# Estado inicial e objetivo
initialState = [[1, 2, 3], [0, 6, 4], [8, 7, 5]]
goalState = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

print("\nEstados das listas de nodos abertos e fechados: \n")
aStarResult = AStarSearch()
print("Árvore de busca: \n")
DrawSearchTree(aStarVisited)
print("Caminho encontrado: ")
PrintSearchPath(aStarResult)