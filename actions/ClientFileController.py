import os
import json


class ClientFileController:

    def __init__(self):
        self.__users_data_file_path = os.path.abspath('data/clients.json')

    def open_clients_data_file(self):
        f = open(self.__users_data_file_path)
        data = json.load(f)
        f.close()
        return data

    def find_client_by_login(self, login):
        clients = self.open_clients_data_file()
        if login in clients:
            return clients[login]
        print("Client with provided login doesn't exist")

    def find_client_by_login_and_password(self, login, password):
        data = self.open_clients_data_file()
        if login in data:
            if data[login]['password'] == password:
                print('user with provided login and password exist')
                return True
        print("Client with provided login or password doesn't exist")
        return False

    def transfer_money_to_account(self, from_client_account_id, account_nr, value):
        clients = self.open_clients_data_file()
        for key in clients:
            if account_nr in clients[key]['account_nr']:
                if clients[from_client_account_id]['account_nr'] == clients[key]['account_nr']:
                    return 'Can not transfer money to the same account'
                if self.check_for_enough_money(from_client_account_id, value):
                    self.manipulate_money_to_selected_client(clients[key], value, 'add')
                    self.manipulate_money_to_selected_client(clients[from_client_account_id], value, 'remove')
                    return 'account with given number exist. Transfering..'
                else:
                    return 'You don\'t have enough money'
                break

    def manipulate_money_to_selected_client(self, client, value, operation):
        with open(self.__users_data_file_path, 'r') as file:
            clients = json.load(file)
            for key in clients:
                if clients[key] == client:
                    if operation == 'add':
                        clients[key]['balance'] = clients[key]['balance'] + float(value)
                    if operation == 'remove':
                        clients[key]['balance'] = clients[key]['balance'] - float(value)
        with open(self.__users_data_file_path, 'w') as file:
            json.dump(clients, file)

    def check_for_enough_money(self, client_id, value):
        clients = self.open_clients_data_file()
        if self.find_client_by_login(client_id):
            if clients[client_id]['balance'] >= float(value):
                return True
            else:
                return False

    def show_account_balance(self, client_id):
        clients = self.open_clients_data_file()
        if self.find_client_by_login(client_id):
            return clients[client_id]['balance']
