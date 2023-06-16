# Problema do Quebra-Cabeça de 8
# 0 foi usado para representar o espaço vazio

class Node:
    def __init__(self, parent, state, cost):
        self.parent = parent
        self.state = state
        self.cost = cost

    def GenerateNewNodes(self):
        newNodes = []

        emptyIndex = GetEmptyIndex(self.state)
        row = emptyIndex // 3
        col = emptyIndex % 3
        
        # Movimento para cima
        if row > 0:
            newState = self.state.copy()
            newState[emptyIndex] = newState[emptyIndex - 3]
            newState[emptyIndex - 3] = 0
            newNodes.append(Node(self, newState, h(newState)))

        # Movimento para baixo
        if row < 2:
            newState = self.state.copy()
            newState[emptyIndex] = newState[emptyIndex + 3]
            newState[emptyIndex + 3] = 0
            newNodes.append(Node(self, newState, h(newState)))

        # Movimento para esquerda
        if col > 0:
            newState = self.state.copy()
            newState[emptyIndex] = newState[emptyIndex - 1]
            newState[emptyIndex - 1] = 0
            newNodes.append(Node(self, newState, h(newState)))

        # Movimento para direita
        if col < 2:
            newState = self.state.copy()
            newState[emptyIndex] = newState[emptyIndex + 1]
            newState[emptyIndex + 1] = 0
            newNodes.append(Node(self, newState, h(newState)))

        return newNodes
        
    def __eq__(self, __value: object) -> bool:
        return self.state == __value.state
    
def GetEmptyIndex(state):
    return state.index(0)

def h(state):
    distance = 0
    for i in range(len(state)):
        if state[i] != goalState[i]:
            distance += 1
    return distance
    
def GreedyBestFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, initialState, 0))

    while len(openNodes) > 0:
        print("Nodos abertos: ", [n.state for n in openNodes])
        print("Nodos fechados: ", [n.state for n in closedNodes])
        openNodes.sort(key=lambda x: x.cost)
        node = openNodes.pop(0)
        closedNodes.append(node)

        if node.state == goalState:
            return node

        for childNode in node.GenerateNewNodes():
            validNodes = []
            if childNode not in openNodes and childNode not in closedNodes:
                validNodes.append(childNode)            
            openNodes = validNodes + openNodes

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
            print(node.state[0:3])
            print(node.state[3:6])
            print(node.state[6:9])
            print()
    else:
        print("Não foi possível encontrar uma solução.")

# Estado inicial e objetivo
initialState = [1, 3, 4, 8, 2, 5, 7, 6, 0]
goalState = [1, 2, 3, 8, 0, 4, 7, 6, 5]

gbfs = GreedyBestFirstSearch()

# Imprime o caminho encontrado
print("Caminho encontrado: ")
PrintSearchPath(gbfs)
print("Custo da busca gulosa pela melhor escolha: ", SearchCostCalculator(gbfs))
