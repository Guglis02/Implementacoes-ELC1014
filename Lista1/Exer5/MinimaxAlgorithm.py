# Dados 10 palitos cada jogador pode retirar 1, 2 ou 3 por turno. Perde o jogador que retira o último palito.


class Node:
    def __init__(self, parent, gameState, IsMaxTurn):
        self.parent = parent
        self.gameState = gameState
        self.IsMaxTurn = IsMaxTurn

    def GenerateNewNodes(self):
        newNodes = []

        # Remove 1 palito
        if self.gameState > 1:
            newNodes.append(Node(self, self.gameState - 1, not self.IsMaxTurn))

        # Remove 2 palitos
        if self.gameState > 2:
            newNodes.append(Node(self, self.gameState - 2, not self.IsMaxTurn))

        # Remove 3 palitos
        if self.gameState > 3:
            newNodes.append(Node(self, self.gameState - 3, not self.IsMaxTurn))

        return newNodes

    def evaluate(self):
        if self.gameState == 1:
            if self.IsMaxTurn:
                return -1
            else:
                return 1
        return 0
        
    def __eq__(self, __value: object) -> bool:
        return self.gameState == __value.gameState
 
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
            print(node.IsMaxTurn, "   ", node.gameState)
    else:
        print("Não foi possível encontrar uma solução.")

def Minimax():
    openNodes = []
    closedNodes = []

    openNodes.append(Node(None, 10, True))

    while len(openNodes) > 0:
        node = openNodes.pop(0)

        if node.gameState == 1:
            return node
        
        closedNodes.append(node)

        if node.IsMaxTurn:
            bestValue = float('-inf')
            bestNode = None

            newNodes = node.GenerateNewNodes()
            for newNode in newNodes:
                value = Minimax(newNode).evaluate()
                if value > bestValue:
                    bestValue = value
                    bestNode = newNode

            return bestNode
        else:
            bestValue = float('inf')
            bestNode = None

            newNodes = node.GenerateNewNodes()
            for newNode in newNodes:
                value = Minimax(newNode).evaluate()
                if value < bestValue:
                    bestValue = value
                    bestNode = newNode

            return bestNode


        newNodes = node.GenerateNewNodes()
        for newNode in newNodes:
            if newNode not in openNodes and newNode not in closedNodes:
                openNodes.append(newNode)
    return None

initialState = 10
finalState = 0

result = Minimax()

print("Caminho encontrado: ")
PrintSearchPath(result)