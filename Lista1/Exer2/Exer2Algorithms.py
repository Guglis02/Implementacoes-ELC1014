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

# Classe que representa um nó da estrutura
class Node:
    def __init__(self, parent, city, flight):
        self.parent = parent
        self.city = city
        self.flight = flight

    # Gera os novos nós a partir do estado atual
    def GenerateNewNodes(self):
        newNodes = []

        for i in range(19):   
            if self.city == operations[i][1]:         
                newNode = Node(self, operations[i][2], operations[i][0])
                newNodes.append(newNode)

        return newNodes
        
    def __eq__(self, __value: object) -> bool:
        return self.city == __value.city
    
    def __hash__(self):
        return hash(tuple(self.city))
    
dfsVisited = []
# Busca em profundidade
def DepthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, initialCity, "Cidade Inicial"))

    print("\nEstados das listas de nodos abertos e fechados usada pelo algoritmo de busca em profundidade: \n")
    while len(openNodes) > 0:
        node = openNodes.pop(0)
        dfsVisited.append(node)
        closedNodes.append(node)

        if node.city == goalCity:
            return node

        for childNode in node.GenerateNewNodes():
            validNodes = []
            if childNode not in openNodes and childNode not in closedNodes:
                validNodes.append(childNode)            
            openNodes = validNodes + openNodes
            
        print("Nodos abertos: ", [n.flight for n in openNodes])
        print("Nodos fechados: ", [n.flight for n in closedNodes])

    return None

bfsVisited = []
# Busca em largura
def BreadthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, initialCity, "Cidade Inicial"))

    print("\nEstados das listas de nodos abertos e fechados usada pelo algoritmo de busca em largura: \n")
    while len(openNodes) > 0:
        node = openNodes.pop(0)
        bfsVisited.append(node)
        closedNodes.append(node)

        if node.city == goalCity:
            return node

        for childNode in node.GenerateNewNodes():
            if childNode not in openNodes and childNode not in closedNodes:
                openNodes.append(childNode)

        print("Nodos abertos: ", [n.flight for n in openNodes])
        print("Nodos fechados: ", [n.flight for n in closedNodes])

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
        print(node.city)
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
        print(prefix[:-1] + "└── " + node.flight)
    else:
        print(node.flight)

    if node in node_map:
        children = node_map[node]
        for i, child in enumerate(children):
            if i == len(children) - 1:
                RecursiveDraw(node_map, child, prefix + "    ")
            else:
                RecursiveDraw(node_map, child, prefix + "│   ")

# Estado inicial e objetivo
initialCity = "a"
goalCity = "j"

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