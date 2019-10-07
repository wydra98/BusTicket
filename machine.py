from tkinter import *
from tkinter import messagebox
from exceptions import *

class Coin:
    coins = [1,2,5,10,20,50,100,200,500,1000,2000,5000]
    def __init__(self, value):
        for coin in self.coins:
            if coin == value:
                self.value = value
                break
            else:
                self.value = 0

class Ticket:
    def __init__(self):
        self.list_ticket=[]
        self.tickets = [140,190,280,380,250,500]
        self.buy_ticket = {x: 0 for x in self.tickets}
        self.prize=0
        self.amount_ticket=0

    def addTickets(self, value):
        try:
            if self.buy_ticket[value] > 98:
               raise ToMuchTicketError
        except ToMuchTicketError:
            messagebox.showerror(title="UWAGA", message="Za dużo biletów.")
        else:
            self.list_ticket.append(value)
            self.buy_ticket[value]+=1
            self.amount_ticket = 0
            self.prize=0
            for self.x in self.list_ticket:
                self.prize += self.x
            self.amount_ticket = self.prize/100

    def delTicket(self, value):
        try:
            if self.buy_ticket[value] < 1:
                raise ToSmallTicketError
        except ToSmallTicketError:
            messagebox.showerror(title="UWAGA", message="Tylko dodatnia liczba biletów.")
        else:
            self.list_ticket.remove(value)
            self.buy_ticket[value] -= 1
            self.amount_ticket = 0
            self.prize = 0
            for self.x in self.list_ticket:
                self.prize += self.x
            self.amount_ticket = self.prize/100

class Machine:
    def __init__(self):
        self.list_coins=[]
        self.throw_coin = {x: 0 for x in Coin.coins}
        self.inside_machine = {}
        self.default_coins_in_machine()
        self.number_of_nominals = 1
        self.i = 0
        self.amount_coins=0

    def my_generator(self):
        yield 3     #1
        yield 3     #2
        yield 0     #5
        yield 0     #10
        yield 0     #20
        yield 0     #50
        yield 0     #100
        yield 0     #200
        yield 0     #500
        yield 0     #1000
        yield 0     #2000
        yield 0     #5000

    def default_coins_in_machine(self):
        generator = self.my_generator() #zwracamy obiekt generatora,wywołując funkcję generującą
        for x in(1,2,5,10,20,50,100,200,500,1000,2000,5000):
            self.inside_machine[x]= next(generator)

    def add_number_nominals(self, number_of_nominals):
        self.i = 0
        self.number_of_nominals = number_of_nominals
        for self.x in self.list_coins:
            self.inside_machine[self.x] = self.inside_machine[self.x] - self.throw_coin[self.x]
            self.throw_coin[self.x] = 0
        self.amount_coins = 0
        self.list_coins = []

    def add_coin(self, coin):
        if self.i < self.number_of_nominals:
            self.list_coins.append(coin)
            self.throw_coin[coin] += 1
            print("WRZUCONE:    ", machine.throw_coin)
            self.inside_machine[coin] += 1
            print("AUTOMAT:     ", machine.inside_machine)
            self.amount_coins = 0
            self.sum = 0
            for self.x in self.list_coins:
                self.sum += self.x
            self.amount_coins = self.sum/100
        self.i = self.i + 1

machine = Machine()
ticket = Ticket()

