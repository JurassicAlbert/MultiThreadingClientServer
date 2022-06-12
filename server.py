import socket
from threading import Thread

# http://net-informations.com/python/net/thread.htm
# with code refactor
# new features added
# changed to provide functionalities required from project 1
from Actions.ClientFileController import ClientFileController
from Actions.UserController import UserController
from data.MessageData import MessageData


class Server(Thread):

    def __init__(self, client_socket: socket, client_address: str):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_file = ClientFileController()
        self.client_actions = UserController()
        self.message_data = MessageData()
        print("New connection added: ", client_address)

    def run(self):
        print("Connection from : ", client_address)
        # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            self.send_message_to_client(self.message_data.welcome_message)
            msg_from_client = self.get_message_from_client()

            print('chosed option: ', msg_from_client)
            if msg_from_client == '1':
                self.send_message_to_client("Insert your login and password")
                client_login = self.get_message_from_client()
                client_password = self.get_message_from_client()

                if not self.client_file \
                        .find_client_by_login_and_password(client_login, client_password):
                    self.send_message_to_client('2')
                    print('unable to find client with given login.. '
                          'closing client with address', client_address)
                    break
                else:
                    self.send_message_to_client('User logged in.')
                    self.send_message_to_client(self.message_data.client_available_options)
                    while True:
                        request_from_client = self.get_message_from_client()
                        print('Selected option: ', request_from_client)
                        if request_from_client == '5':
                            print("Client at ", client_address, " disconnected...")
                            break
                        if request_from_client == '1':
                            #send account balance
                            self.send_message_to_client('Account Balance: '+str(self.client_file.show_account_balance(client_login)))
                        if request_from_client == '2':
                            self.send_message_to_client('Account Balance'
                                                        + str(self.client_file.show_account_balance(client_login)))
                            self.send_message_to_client('How many money do you want to deposit? ')
                            money = self.get_message_from_client()
                            self.client_actions.deposit_money(client_login, money)
                            self.send_message_to_client(
                                'Account Balance: ' + str(self.client_file.show_account_balance(client_login)))
                        if request_from_client == '3':
                            self.send_message_to_client('Account Balance'
                                                        + str(self.client_file.show_account_balance(client_login)))
                            self.send_message_to_client('How many money do you want to withdraw? ')
                            money = self.get_message_from_client()
                            self.client_actions.withdraw_money(client_login, money)
                        if request_from_client == '4':
                            self.send_message_to_client(
                                'Account Balance Before Transfer: '
                                + str(self.client_file.show_account_balance(client_login)))
                            self.send_message_to_client('How many money do you want to transfer? ')
                            money = self.get_message_from_client()
                            self.send_message_to_client('Where do you want to transfer your money (account number)? ')
                            account_nr = self.get_message_from_client()
                            transfer = self.client_file.transfer_money_to_account(client_login, account_nr, money)
                            print(transfer)
                            self.send_message_to_client(transfer)

                        break

            if msg_from_client == '2':
                break

        print("Client at ", client_address, " disconnected...")

    def send_message_to_client(self, message):
        self.client_socket.send(bytes(message, 'UTF-8'))

    def get_message_from_client(self):
        data_from_user = self.client_socket.recv(2048)
        return data_from_user.decode()

    def get_selected_client(self, login):

        pass


LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    client_socket, client_address = server.accept()
    new_thread = Server(client_socket, client_address)

    new_thread.start()
