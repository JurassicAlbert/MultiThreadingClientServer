import socket
from threading import Thread
from actions.ClientFileController import ClientFileController
from actions.UserController import UserController
from data.MessageData import MessageData


class ServerThread(Thread):

    def __init__(self, client_socket: socket, client_address: str):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_file = ClientFileController()
        self.client_actions = UserController()
        self.message_data = MessageData()
        self.client_address = client_address
        print("New connection added: ", client_address)

    def run(self):
        print("Connection from : ", self.client_address)
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
                          'closing client with address', self.client_address)
                    break
                else:
                    self.send_message_to_client('User logged in.')
                    self.send_message_to_client(self.message_data.client_available_options)
                    while True:
                        request_from_client = self.get_message_from_client()
                        print('Selected option: ', request_from_client)
                        if request_from_client == '5':
                            print("Client at ", self.client_address, " disconnected...")
                            break
                        if request_from_client == '1':
                            # send account balance
                            self.send_message_to_client(
                                'Account Balance: ' + str(self.client_file.show_account_balance(client_login)))
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

        print("Client at ", self.client_address, " disconnected...")

    def send_message_to_client(self, message):
        self.client_socket.send(bytes(message, 'UTF-8'))

    def get_message_from_client(self):
        data_from_user = self.client_socket.recv(2048)
        return data_from_user.decode()
