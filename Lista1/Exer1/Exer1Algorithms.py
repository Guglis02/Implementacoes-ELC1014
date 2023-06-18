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

# Formata o estado para exibição
FormatState = lambda state: "[" + \
    ("E" if state[0] else "D") + ", " + \
    ("E" if state[1] else "D") + ", " + \
    ("E" if state[2] else "D") + ", " + \
    ("E" if state[3] else "D") + "]"

# Classe que representa um nó da estrutura
class Node:
    def __init__(self, parent, state, action):
        self.parent = parent
        self.state = state
        self.action = action

    # Se a Ovelha não está sozinha com o repolho o com o lobo, o estado é válido
    def IsValid(self):
        if self.state[0] != self.state[2] and (self.state[1] == self.state[2] or self.state[3] == self.state[2]):
            return False
        return True
    
    # Gera os novos nós a partir do estado atual
    def GenerateNewNodes(self):
        newNodes = []

        for i in range(4):
            if self.state[0] == self.state[i]:
                newNode = Node(self, actions[i][1](self.state), actions[i][0])
                if newNode.IsValid():
                    newNodes.append(newNode)

        return newNodes
        
    def __eq__(self, __value: object) -> bool:
        return self.state == __value.state
    
    def __hash__(self):
        return hash(tuple(self.state))
    
dfsVisited = []
# Busca em profundidade
def DepthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, initialState, "Estado Inicial"))

    print("\nEstados das listas de nodos abertos e fechados usada pelo algoritmo de busca em profundidade: \n")
    while len(openNodes) > 0:
        node = openNodes.pop(0)
        dfsVisited.append(node)
        closedNodes.append(node)

        if node.state == goalState:
            return node

        for childNode in node.GenerateNewNodes():
            validNodes = []
            if childNode not in openNodes and childNode not in closedNodes:
                validNodes.append(childNode)            
            openNodes = validNodes + openNodes
            
        print("Nodos abertos: ", [FormatState(n.state) for n in openNodes])
        print("Nodos fechados: ", [FormatState(n.state) for n in closedNodes])

    return None

bfsVisited = []
# Busca em largura
def BreadthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, initialState, "Estado Inicial"))

    print("\nEstados das listas de nodos abertos e fechados usada pelo algoritmo de busca em largura: \n")
    while len(openNodes) > 0:
        node = openNodes.pop(0)
        bfsVisited.append(node)
        closedNodes.append(node)

        if node.state == goalState:
            return node

        for childNode in node.GenerateNewNodes():
            if childNode not in openNodes and childNode not in closedNodes:
                openNodes.append(childNode)

        print("Nodos abertos: ", [FormatState(n.state) for n in openNodes])
        print("Nodos fechados: ", [FormatState(n.state) for n in closedNodes])

    return None

# Método para imprimir o caminho da solução
def PrintSearchPath(result):
    aux = result
    path = []
    path.append(aux)

    while aux.parent is not None:
        aux = aux.parent
        path.append(aux)

    path.reverse()

    for node in path:
        print(node.action)
        print(FormatState(node.state))
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
        print(prefix[:-1] + "└── " + node.action)
    else:
        print(node.action)

    if node in node_map:
        children = node_map[node]
        for i, child in enumerate(children):
            if i == len(children) - 1:
                RecursiveDraw(node_map, child, prefix + "    ")
            else:
                RecursiveDraw(node_map, child, prefix + "│   ")

# Estado inicial e objetivo
initialState = [True, True, True, True]
goalState = [False, False, False, False]

# Chama as buscas
bfsResult = BreadthFirstSearch()
dfsResult = DepthFirstSearch()

# Desenha as arvores de busca
print("\n\nÁrvore de busca criada pelo algoritmo de busca em largura:")
DrawSearchTree(bfsVisited)
print("\n\nÁrvore de busca criada pelo algoritmo de busca em profundidade:")
DrawSearchTree(dfsVisited)

# Imprime os caminhos encontrados
if bfsResult is not None:
    print("\nPasso a passo encontrado pelo algoritmo de busca em largura: ")
    PrintSearchPath(bfsResult)
else:
    print("Não foi possível encontrar uma solução.")

if dfsResult is not None:
    print("\nPasso a passo encontrado pelo algoritmo de busca em largura: ")
    PrintSearchPath(dfsResult)
else:
    print("Não foi possível encontrar uma solução.")