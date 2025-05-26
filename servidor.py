import socket
import sys

def main():
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco = ('127.0.0.1', 50000)
    conexao.bind(endereco)
    conexao.listen(2)

    players = []
    while len(players) < 2:
        socket_player, _ = conexao.accept()
        player = "X" if len(players) == 0 else "O"
        socket_player.send(player.encode())
        players.append(socket_player)

    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
    colunas = 'a', 'b', 'c'
    player_atual = None

    while True:
        
        if player_atual == players[0]:
            player_atual = players[1]
        else:
            player_atual = players[0]

        enviar_tabuleiro(tabuleiro, players)

        while True:
            msg = int.to_bytes(1, 1, 'big')
            player_atual.send(msg)
            resposta = player_atual.recv(2)
            if not resposta:
                print('Falha ao receber a jogada')
                sys.exit(-1)
            
            coordenadas = resposta.decode()
            if len(coordenadas) == 2 and coordenadas[0] in colunas and coordenadas[1].isdigit() and 1 <= int(coordenadas[1]) <= 3 and tabuleiro[colunas.index(coordenadas[0])][int(coordenadas[1]) - 1] == " ":
                    tabuleiro[colunas.index(coordenadas[0])][int(coordenadas[1]) - 1] = "X" if player_atual == players[0] else "O"
                    break
        
        if vitoria(tabuleiro):
            msg = int.to_bytes(2, 1, 'big') + int.to_bytes(0, 1, 'big') if player_atual == players[0] else int.to_bytes(1, 1, 'big')
            for p in players:
                p.send(msg)
            break
        
        if empate(tabuleiro):
            msg = int.to_bytes(3, 1, 'big')
            for p in players:
                p.send(msg)
            break



def vitoria(tabuleiro):
    # Verifica colunas
    for linha in tabuleiro:
        if all(c == linha[0] and c != " " for c in linha):
            return True

    # Rotaciona e verifica colunas
    rotated = [list(linha) for linha in zip(*tabuleiro)]
    rotated = [list(reversed(linha)) for linha in rotated]
    for linha in rotated: 
        if all(c == linha[0] and c != " " for c in linha):
            return True
        
    # Verifica diagonais
    for x, y in zip((0, 2), (2, 0)): 
        if tabuleiro[0][x] == tabuleiro[1][1] == tabuleiro[2][y] != " ":
            return True
                
def empate(tabuleiro):
    if all(c != " " for linha in tabuleiro for c in linha):
        return True
    return False

        
def enviar_tabuleiro(tabuleiro, players):
    texto = ''.join(c for linha in tabuleiro for c in linha)
    msg = int.to_bytes(0, 1, 'big') + len(texto.encode()).to_bytes(1, 'big') + texto.encode()
    for p in players:
        p.send(msg)

if __name__ == '__main__':
    main()