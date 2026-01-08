from interfaces import IUserInterface

class ConsoleUI(IUserInterface) :
    def display(self, message) :
        print(message)