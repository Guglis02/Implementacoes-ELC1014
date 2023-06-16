# Como cada elemento pode estar apenas em dois estados, cada valor é representado como um booleano,
# onde True significa que o elemento está na margem esquerda e False significa que o elemento está na margem direita.

# Define as ações e os operadores
# A mudança de margem é feita usando o operador not
actions = [
    ("Atravessa Fazendeiro", lambda state: [not state[0], state[1], state[2], state[3]]),
    ("Atravessa Lobo", lambda state: [not state[0], not state[1], state[2], state[3]]),
    ("Atravessa Ovelha", lambda state: [not state[0], state[1], not state[2], state[3]]),
    ("Atravessa Repolho", lambda state: [not state[0], state[1], state[2], not state[3]])
]

# Define se deve imprimir o caminho até o objetivo
shouldPrintPath = True
# Define se deve imprimir os estados abertos e fechados ao longo da busca
shouldPrintStates = False

class Node:
    def __init__(self, action, state, parent):
        self.action = action
        self.state = state
        self.parent = parent

    def IsValid(self):
        if self.state[0] != self.state[2] and (self.state[1] == self.state[2] or self.state[3] == self.state[2]):
            return False
        return True
    
    def GenerateNewNodes(self):
        newNodes = []

        for i in range(4):
            if self.state[0] == self.state[i]:
                newNode = Node(actions[i][0], actions[i][1](self.state), self)
                if newNode.IsValid():
                    newNodes.append(newNode)

        return newNodes
        
    def __eq__(self, __value: object) -> bool:
        return self.state == __value.state
    
def DepthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node("Estado Inicial", initial_state, None))

    while len(openNodes) > 0:
        if shouldPrintStates:
            print("Nodos abertos: ", [n.state for n in openNodes])
            print("Nodos fechados: ", [n.state for n in closedNodes])
        node = openNodes.pop(0)
        closedNodes.append(node)

        if node.state == goal_state:
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

    openNodes.append(Node("Estado Inicial", initial_state, None))

    while len(openNodes) > 0:
        if shouldPrintStates:
            print("Nodos abertos: ", [n.state for n in openNodes])
            print("Nodos fechados: ", [n.state for n in closedNodes])
        node = openNodes.pop(0)
        closedNodes.append(node)

        if node.state == goal_state:
            return node

        for childNode in node.GenerateNewNodes():
            if childNode not in openNodes and childNode not in closedNodes:
                openNodes.append(childNode)

    return None

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
            print(node.action)
            print(node.state)
    else:
        print("Não foi possível encontrar uma solução.")

# Estado inicial e objetivo
initial_state = [True, True, True, True]
goal_state = [False, False, False, False]

# Chama a busca em profundidade
result = BreadthFirstSearch()

# Imprime o caminho encontrado
if result is not None:
    if shouldPrintPath:
        PrintSearchPath(result)
else:
    print("Não foi possível encontrar uma solução.")
