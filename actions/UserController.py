# toys goes here
from actions.ClientFileController import ClientFileController


class UserController:

    def __init__(self):
        self.clientFile = ClientFileController()

    def withdraw_money(self, existing_client_id, value):
        existing_client = self.clientFile.find_client_by_login(existing_client_id)
        self.clientFile.manipulate_money_to_selected_client(existing_client, value, 'remove')

    def deposit_money(self, existing_client_id, value):
        existing_client = self.clientFile.find_client_by_login(existing_client_id)
        self.clientFile.manipulate_money_to_selected_client(existing_client, value, 'add')
