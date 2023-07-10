import os
from socket import *

from Client import Client

class Player:
    def __init__(self):
        self.__name = ""
        self.client = Client()
        self.last_server_message=""
        self.game_status = 0
        self.message=""
        self.life = 100
        self.argument = 0
        self.score = 0

    def set_name(self,name):
        self.__name = name

    def recive(self):
        result=self.last_server_message.decode().split(';')
        if len(result) ==3:
            self.message = result[0]
            self.life = int(result[1])
            self.score = int(result[2])
        elif len(result) ==4:
            self.message= result[0]
            self.argument = int(result[1])
            self.life= int(result[2])
            self.score = int(result[3])
        else: 
            self.message = result[0]


    def start(self):
        self.last_server_message = self.client.send_command("START")
        self.recive()
        self.game_status=1


    def run(self):
        self.last_server_message = self.client.send_command("RUN")
        self.recive()

    def yes(self):
        self.last_server_message = self.client.send_command("YES")
        self.recive()
    
    def no(self):
        self.last_server_message = self.client.send_command("NO")
        self.recive()

    def walk(self):
        self.last_server_message = self.client.send_command("WALK")
        self.recive()

    def fight(self):
        self.last_server_message = self.client.send_command("FIGHT")
        self.recive()

    def send_number(self,number):
        self.last_server_message = self.client.send_command(str(number))
        self.recive()

    def exit(self):
        self.client.close_connection()



    def server_message(self):
        if self.message == 'MONSTER_ATTACK':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você foi atacado por um monstro escondido!")
            n = int(input(f"Escolha um numero entre 0 e {self.argument }: "))
            self.send_number(n)
            self.recive()
            

        elif self.message == "MONSTER_KILLED":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Parabens, voce matou o monstro ")
            print(f"{self.message} Sua vida: {self.life}. Sua pontuação: {self.score}.")
            print("Pressione Enter para continuar...")
            input()
            self.walk()
            self.recive()
            

        elif self.message == "MONSTER_ATTACKED":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Não foi dessa vez, você sofreu dano")
            print(f"{self.message} Sua vida: {self.life}. Sua pontuação: {self.score}.")
            print("Pressione Enter para continuar...")
            input()
            self.walk()
            self.recive()
            

        elif self.message == "TAKE_CHEST":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("você encontou um bau")
            n = input("Deseja abri-lo? (S/N): ").upper()
            if n== 'S':
                self.yes()
            else:
                self.no()
            self.recive()

        elif self.message == "CHEST_VALUE":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você abriu o Bau")
            self.walk()
            self.recive()
            print(f"{self.message} Sua vida: {self.life}. Sua pontuação: {self.score}.")
            print("Pressione Enter para continuar...")
            input()

        elif self.message =="SKIPPING_CHEST":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você Ignorou o Bau")
            self.walk()
            self.recive()
            print("Pressione Enter para continuar...")
            input()

        elif self.message =="BOSS_EVENT":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você encontrou um chefão:")
            n = input("Deseja atacar ou fugir? (A/F): ")
            if n== 'A':
                self.fight()
            else:
                self.run()
            self.recive()

        elif self.message =="ESCAPED":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você ficou com medo e fugiu, mas conseguiu escapar com sucesso.")
            print(f"{self.message} Sua vida: {self.life}. Sua pontuação: {self.score}.")
            print("Pressione Enter para continuar...")
            input()
            self.walk()
            self.recive()
            
        elif self.message =="BOSS_DEFEATED":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você venceu o chefão, PARABÉNS")
            print(f"{self.message} Sua vida: {self.life}. Sua pontuação: {self.score}.")
            print("Pressione Enter para continuar...")
            input()
            self.walk()
            self.recive()

        elif self.message =="FAILED_BOSS_FIGHT":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você foi valente, mas não ganhou essa batalha, siga em frente.")
            print(f"{self.message} Sua vida: {self.life}. Sua pontuação: {self.score}.")
            print("Pressione Enter para continuar...")
            input()
            self.walk()
            self.recive()


        elif self.message =="NOTHING_HAPPENED":
            print("---------------") # i dont now 
            os.system('cls' if os.name == 'nt' else 'clear')
            self.walk()
            self.recive()

        elif self.message =="WIN":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("WINNER")
            self.game_status=0
            self.recive()
            self.exit()

        elif self.message =="GAME_OVER":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Game Over")
            self.game_status=0
            self.recive()
            self.exit()



    



