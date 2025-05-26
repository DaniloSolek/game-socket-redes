import socket
import sys

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 50000))

    msg = sock.recv(2)
    if not msg:
        print('Erro de conexão')
        sys.exit(-1)

    player = msg.decode(encoding='utf-8')
    print('Você é o player', player)

    colunas = 'a', 'b', 'c'
    fim = False
    while not fim:
        msg = sock.recv(1)
        if not msg:
            print('Desconexão')
            sys.exit(-1)
        
        codigo = int.from_bytes(msg, 'big')

        match codigo:
            # Recebe o tabuleiro
            case 0:
                tam = int.from_bytes(sock.recv(1), 'big')
                tabuleiro = sock.recv(tam).decode()
                matriz = [list(tabuleiro[i*3:(i+1)*3]) for i in range(3)]
                show(matriz, colunas)
            # Servidor pede jogada
            case 1:
                while True:
                    coordenadas = input(f"Insira as coordenadas\n").lower()
                    if len(coordenadas) == 2 and coordenadas[0] in colunas and coordenadas[1] in "123":
                        break
                    print("Coordenadas inválidas")
                msg = coordenadas.encode()
                sock.send(msg)
            case 2:
                vencedor = "X" if int.from_bytes(sock.recv(1), 'big') == 0 else "O"
                if vencedor == player:
                    print('Você venceu!')
                else:
                    print('Você perdeu!')
                fim = True
            case 3:
                print('Empate!')
                fim = True


def show(tabuleiro, colunas):
    print("   1   2   3 \n  ---+---+---")
    for column, row in zip(colunas, tabuleiro):
        print(f"{column}  {" | ".join(row)} \n  ---+---+---")

if __name__ == '__main__':
    main()