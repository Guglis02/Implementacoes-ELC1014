# Como cada elemento pode estar apenas em dois estados, cada valor é representado como um booleano,
# onde True significa que o elemento está na margem esquerda e False significa que o elemento está na margem direita.

# Define as ações e os operadores
# A mudança de margem é feita usando o operador not
actions = [
    ("atravessaFazendeiro", lambda state: [not state[0], state[1], state[2], state[3]]),
    ("atravessaLobo", lambda state: [not state[0], not state[1], state[2], state[3]]),
    ("atravessaOvelha", lambda state: [not state[0], state[1], not state[2], state[3]]),
    ("atravessaRepolho", lambda state: [not state[0], state[1], state[2], not state[3]])
]


class Node:
    def __init__(self, state, parent):
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
                newNode = Node(actions[i][1](self.state), self)
                if newNode.IsValid():
                    newNodes.append(newNode)

        return newNodes
        
    def __eq__(self, __value: object) -> bool:
        return self.state == __value.state
    
def DepthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(initial_state, None))

    while len(openNodes) > 0:
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

    openNodes.append(Node(initial_state, None))

    while len(openNodes) > 0:
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

# Estado inicial e objetivo
initial_state = [True, True, True, True]
goal_state = [False, False, False, False]

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
        print(node.state)
else:
    print("Não foi possível encontrar uma solução.")
