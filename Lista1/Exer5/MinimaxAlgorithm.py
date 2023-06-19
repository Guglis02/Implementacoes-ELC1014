# Dados 10 palitos cada jogador pode retirar 1, 2 ou 3 por turno. 
# Perde o jogador que retira o último palito.

# Classe que representa um nó da estrutura
class Node:
    def __init__(self, parent, gameState, IsMaxTurn):
        self.parent = parent
        self.gameState = gameState
        self.IsMaxTurn = IsMaxTurn

    def GenerateNewNodes(self):
        newNodes = []

        # Remove 1 palito
        if self.gameState >= 1:
            newNodes.append(Node(self, self.gameState - 1, not self.IsMaxTurn))

        # Remove 2 palitos
        if self.gameState >= 2:
            newNodes.append(Node(self, self.gameState - 2, not self.IsMaxTurn))

        # Remove 3 palitos
        if self.gameState >= 3:
            newNodes.append(Node(self, self.gameState - 3, not self.IsMaxTurn))

        return newNodes

    def evaluate(self):
        if self.IsMaxTurn:
            return 1
        else:
            return -1
        
    def __eq__(self, __value: object) -> bool:
        return self.gameState == __value.gameState
 
# Função minimax
def minimax(node, depth, isMaxTurn, indent=0):
    # Verifica se o jogo acabou ou se chegou na profundidade máxima
    if node.gameState == 0 or depth == 0:
        return node.evaluate()

    # Define o valor inicial do melhor valor de acordo com o jogador atual
    bestValue = float('-inf') if isMaxTurn else float('inf')

    # Imprime o estado atual da árvore de busca com o valor de min e max propagados
    print(f"{' ' * indent}GameState: {node.gameState}, {'Vez do MAX' if isMaxTurn else 'Vez do MIN'}")

    # Gera todas as possíveis jogadas
    for child in node.GenerateNewNodes():
        # Chama a função minimax recursivamente para o próximo estado
        value = minimax(child, depth - 1, not isMaxTurn, indent + 4)

        # Atualiza o melhor valor de acordo com o jogador atual
        if isMaxTurn:
            bestValue = max(bestValue, value)
        else:
            bestValue = min(bestValue, value)

    return bestValue

# Define o estado inicial do jogo
initial_state = Node(None, 10, True)

# Chama a função minimax para o estado inicial
bestValue = minimax(initial_state, 10, True)

# Verifica se o jogador MAX ganhou ou perdeu
if bestValue == 1:
    print("MAX ganhou!")
else:
    print("MAX perdeu!")