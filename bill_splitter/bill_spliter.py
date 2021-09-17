import random


class BillSplitter:

    def __init__(self):
        self.n = None
        self.bill = None
        self.friends = {}
        self.lucky_mode = None

    def take_friends(self):
        print('Enter the number of friends joining (including you):')
        self.n = int(input())
        if self.n > 0:
            print("Enter the name of every friend (including you), each on a new line:")
            [self.friends.update({input(): 0}) for _ in range(self.n)]
            print('Enter the total bill value:')
            self.bill = int(input())
            print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
            self.lucky_mode = input()
            if self.lucky_mode == 'Yes':
                lucky_one = random.choice(list(self.friends))
                print(lucky_one + " is the lucky one!")
                divider = len(self.friends) - 1
                portion = round(self.bill / divider, 2)
                self.friends.update((key, portion) for key in self.friends)
                self.friends.update({lucky_one: 0})
                print(self.friends)
            else:
                portion = round(self.bill / len(self.friends), 2)
                self.friends.update((key, portion) for key in self.friends)
                print("No one is going to be lucky")
                print("")
                print(self.friends)
        else:
            print("No one is joining for the party")


def main():
    bill_splitter = BillSplitter()
    bill_splitter.take_friends()


if __name__ == "__main__":
    main()