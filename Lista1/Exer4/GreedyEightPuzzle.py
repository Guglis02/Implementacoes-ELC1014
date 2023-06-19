from copy import deepcopy

# Problema do Quebra-Cabeça de 8
# 0 foi usado para representar o espaço vazio

# Classe que representa um nó da estrutura
class Node:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state

    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(str(self.state))

    # Gera os novos nós a partir do estado atual
    def GenerateNewNodes(self):
        newNodes = []

        emptyIndex = GetIndex(self.state, 0)
        row = emptyIndex[0]
        col = emptyIndex[1]
        
        # Movimento para cima
        if row > 0:
            newState = deepcopy(self.state)
            newState[row][col], newState[row - 1][col] = newState[row - 1][col], newState[row][col]
            newNodes.append(Node(self, newState))

        # Movimento para baixo
        if row < 2:
            newState = deepcopy(self.state)
            newState[row][col], newState[row + 1][col] = newState[row + 1][col], newState[row][col]
            newNodes.append(Node(self, newState))

        # Movimento para esquerda
        if col > 0:
            newState = deepcopy(self.state)
            newState[row][col], newState[row][col - 1] = newState[row][col - 1], newState[row][col]
            newNodes.append(Node(self, newState))

        # Movimento para direita
        if col < 2:
            newState = deepcopy(self.state)
            newState[row][col], newState[row][col + 1] = newState[row][col + 1], newState[row][col]
            newNodes.append(Node(self, newState))

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

greedyVisited = []
# Busca gulosa pela melhor escolha
# Flag usingHeuristic indica se a busca deve usar a função heurística ou custo 1
def GreedyBestFirstSearch(usingHeuristic):
    openNodes = []
    closedNodes = []
    greedyVisited.clear()

    openNodes.append(Node(None, initialState))

    while len(openNodes) > 0:
        if usingHeuristic:
            openNodes.sort(key=lambda x: h(x.state))
        node = openNodes.pop(0)
        greedyVisited.append(node)
        closedNodes.append(node)

        if node.state == goalState:
            return node

        for childNode in node.GenerateNewNodes():
            validNodes = []
            if childNode not in openNodes and childNode not in closedNodes:
                validNodes.append(childNode)            
            openNodes = validNodes + openNodes

        # print("Nodos abertos: ", [n.state for n in openNodes])
        # print("Nodos fechados: ", [n.state for n in closedNodes])

    return None

# Calcula o custo da busca
def SearchCostCalculator(result):
    aux = result
    cost = 1
    while aux.parent is not None:
        cost += 1
        aux = aux.parent
    return cost

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
initialState = [[1, 3, 4], [8, 2, 5], [7, 6, 0]]
goalState = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

# print("Algoritmo de busca gulosa pela melhor escolha usando heurística: \n")
# print("\nEstados das listas de nodos abertos e fechados: \n")    
# gbfshResult = GreedyBestFirstSearch(True)
# print("Árvore de busca: \n")
# DrawSearchTree(greedyVisited)
# print("Caminho encontrado: ")
# PrintSearchPath(gbfshResult)
# print("Custo da busca: ", SearchCostCalculator(gbfshResult))

print("Algoritmo de busca gulosa pela melhor escolha usando custo 1: \n")
print("\nEstados das listas de nodos abertos e fechados: \n")
gbfsResult = GreedyBestFirstSearch(False)
print("Árvore de busca: \n")
DrawSearchTree(greedyVisited)
print("Caminho encontrado: ")
PrintSearchPath(gbfsResult)
print("Custo da busca: ", SearchCostCalculator(gbfsResult))