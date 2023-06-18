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

# Classe que representa um nó da estrutura
class Node:
    def __init__(self, parent, city, cost):
        self.city = city
        self.parent = parent
        self.cost = cost

    # Gera os novos nós a partir do estado atual
    def GenerateNewNodes(self):
        newNodes = []

        for i in range(12):   
            if self.city == operations[i][0]:         
                newNode = Node(self, operations[i][1], operations[i][2])
                newNodes.append(newNode)

        return newNodes
        
    def __eq__(self, __value: object) -> bool:
        return self.city == __value.city
    
    def __hash__(self):
        return hash(tuple(self.city))
    
greedyVisited = []
# Busca gulosa pela melhor escolha 
def GreedyBestFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, initialCity, 0))

    print("\nEstados das listas de nodos abertos e fechados usadas pelo algoritmo de busca gulosa pela melhor escolha: \n")
    while len(openNodes) > 0:
        openNodes.sort(key=lambda x: x.cost)
        node = openNodes.pop(0)
        greedyVisited.append(node)
        closedNodes.append(node)

        if node.city == goalCity:
            return node

        for childNode in node.GenerateNewNodes():
            validNodes = []
            if childNode not in openNodes and childNode not in closedNodes:
                validNodes.append(childNode)            
            openNodes = validNodes + openNodes

        print("Nodos abertos: ", [n.city for n in openNodes])
        print("Nodos fechados: ", [n.city for n in closedNodes])

    return None

dfsVisited = []
# Busca em profundidade
def DepthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, initialCity, 0))

    print("\nEstados das listas de nodos abertos e fechados usadas pelo algoritmo de busca em profundidade: \n")
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

        print("Nodos abertos: ", [n.city for n in openNodes])
        print("Nodos fechados: ", [n.city for n in closedNodes])

    return None

bfsVisited = []
# Busca em largura
def BreadthFirstSearch():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, initialCity, 0))

    print("\nEstados das listas de nodos abertos e fechados usadas pelo algoritmo de busca em largura: \n")
    while len(openNodes) > 0:
        node = openNodes.pop(0)
        bfsVisited.append(node)
        closedNodes.append(node)

        if node.city == goalCity:
            return node

        for childNode in node.GenerateNewNodes():
            if childNode not in openNodes and childNode not in closedNodes:
                openNodes.append(childNode)

        print("Nodos abertos: ", [n.city for n in openNodes])
        print("Nodos fechados: ", [n.city for n in closedNodes])

    return None

# Calcula o custo da busca
def SearchCostCalculator(result):
    aux = result
    cost = 0
    while aux.parent is not None:
        cost += aux.cost
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
        print(prefix[:-1] + "└── " + node.city)
    else:
        print(node.city)

    if node in node_map:
        children = node_map[node]
        for i, child in enumerate(children):
            if i == len(children) - 1:
                RecursiveDraw(node_map, child, prefix + "    ")
            else:
                RecursiveDraw(node_map, child, prefix + "│   ")

# Estado inicial e objetivo
initialCity = "a"
goalCity = "h"

# Chama as buscas
gbfs = GreedyBestFirstSearch()
dfs = DepthFirstSearch()
bfs = BreadthFirstSearch()

# Desenha a árvore de busca do algoritmo de busca gulosa pela melhor escolha
print("\nÁrvore de busca do algoritmo de busca gulosa pela melhor escolha: \n")
DrawSearchTree(greedyVisited)

# Imprime o caminho encontrado
if gbfs is not None:
    print("\nPasso a passo encontrado pelo algoritmo de busca em largura: ")
    PrintSearchPath(gbfs)
else:
    print("Não foi possível encontrar uma solução.")
    
print("Custo da busca gulosa pela melhor escolha: ", SearchCostCalculator(gbfs))
print("Custo da busca em profundidade:", SearchCostCalculator(dfs))
print("Custo da busca em largura:", SearchCostCalculator(bfs))
print()
