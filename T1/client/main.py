from Player import Player

if __name__ == '__main__':
    player = Player()
    player.set_name(input("Insira o nome do seu Jogador\n"))
    player.start()
    while player.game_status==1:
        player.server_message()