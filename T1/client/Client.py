from socket import *

class Client:
    def __init__(self):
        self.serverName = 'localhost'
        self.serverPort = 12000
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def send_command(self, sentence):
        self.clientSocket.send(sentence.encode())
        self.modifiedSentence = self.clientSocket.recv(1024)
        return self.modifiedSentence
        

    def close_connection(self):
        self.clientSocket.close()

    


if __name__ == '__main__':
    cliente = Client()
    cliente.send_command("START")
