def main():
    player1 = "X"
    player2 = "O"
    player_atual = None
    board = [[" " for _ in range(3)] for _ in range(3)]
    colunas = 'a', 'b', 'c'

    while True:

        if player_atual == player1:
            player_atual = player2
        else:
            player_atual = player1
        
        show(board, colunas)
        while True:
            coordenadas = input(f"Player {player_atual}, insira as coordenadas\n").lower()
            if len(coordenadas) == 2 and coordenadas[0] in colunas and coordenadas[1].isdigit() and 1 <= int(coordenadas[1]) <= 3 and board[colunas.index(coordenadas[0])][int(coordenadas[1]) - 1] == " ":
                board[colunas.index(coordenadas[0])][int(coordenadas[1]) - 1] = player_atual
                break
            print('Coordenadas inválidas, tente novamente.\n')
        
        if vitoria(board):
            print(f'Player {player_atual} venceu!')
            break
        if empate(board):
            print('Empate!')
            break

def show(matrix, colunas):
    print("   1   2   3 \n  ---+---+---")
    for column, row in zip(colunas, matrix):
        print(f"{column}  {" | ".join(row)} \n  ---+---+---")

def vitoria(matrix):
    # Verifica colunas
    for row in matrix:
        if all(c == row[0] and c != " " for c in row):
            return True

    # Rotaciona e verifica colunas
    rotated = [list(row) for row in zip(*matrix)]
    rotated = [list(reversed(row)) for row in rotated]
    for row in rotated: 
        if all(c == row[0] and c != " " for c in row):
            return True
        
    # Verifica diagonais
    for x, y in zip((0, 2), (2, 0)): 
        if matrix[0][x] == matrix[1][1] == matrix[2][y] != " ":
            return True

def empate(matrix):
    if all(c != " " for row in matrix for c in row):
        return True
    return False

if __name__ == "__main__":
    main()