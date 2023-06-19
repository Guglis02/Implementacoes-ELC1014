# Dados 10 palitos cada jogador pode retirar 1, 2 ou 3 por turno. 
# Perde o jogador que retira o último palito.

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
 
def minimax(node, depth, is_max_player, indent=0):
    # Verifica se o jogo acabou ou se chegou na profundidade máxima
    if node.gameState == 0 or depth == 0:
        return node.evaluate()

    # Define o valor inicial do melhor valor de acordo com o jogador atual
    best_value = float('-inf') if is_max_player else float('inf')

    # Imprime o estado atual da árvore de busca com o valor de min e max propagados
    print(f"{' ' * indent}GameState: {node.gameState}, {'Vez do MAX' if is_max_player else 'Vez do MIN'}")

    # Gera todas as possíveis jogadas
    for child in node.GenerateNewNodes():
        # Chama a função minimax recursivamente para o próximo estado
        value = minimax(child, depth - 1, not is_max_player, indent + 4)

        # Atualiza o melhor valor de acordo com o jogador atual
        if is_max_player:
            best_value = max(best_value, value)
        else:
            best_value = min(best_value, value)

    return best_value

# Define o estado inicial do jogo
initial_state = Node(None, 10, True)

# Chama a função minimax para o estado inicial
best_value = minimax(initial_state, 10, True)

# Verifica se o jogador MAX ganhou ou perdeu
if best_value == 1:
    print("MAX ganhou!")
else:
    print("MAX perdeu!")