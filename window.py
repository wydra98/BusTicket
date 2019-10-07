from tkinter import *
from machine import *


class Window:
    def __init__(self, master):
        master.title("Bus Ticket Machine")
        master.geometry('790x450+260+150')
        self.master=master
        self.flag=0
        self.text_frame=[]
        self.create_widgets() #tworzenie pierwszego okienka
        self.number_of_nominals = 1
        self.back_from_automat_coins = {} #słownik pomocniczy przy wydawaniu reszty
        self.release_coins = {x: 0 for x in Coin.coins}

    #usuwanie okienka z pieniedmi i odblokowanie funkcji
    def return_to_ticket(self):
        for i in range(6):
            self.text_frame[i].config(state=NORMAL)
            self.button_p_tab[i].config(state=NORMAL)
            self.button_m_tab[i].config(state=NORMAL)
        self.button_pay_1.config(state=NORMAL)
        self.window2.destroy()

    # wyświetlanie wszystkich tekstów typu do zapłaty
    def text_print(self, flag):
        self.text_amount.delete(0.0, END)
        self.text_amount.insert(0.0, "Do zapłaty: " + str(ticket.amount_ticket) + " zł\n")
        if flag == 1:
            self.window2.text.delete(0.0, END)
            self.window2.text.insert(0.0, "Do zapłaty: " + str(ticket.amount_ticket) + " zł\n")
            self.window2.text.insert(CURRENT, "Wrzucono:  " + str(machine.amount_coins) + " zł\n")
            self.window2.text.insert(END, "Liczba nominałów: " + str(self.number_of_nominals))

    #dodawanie monet, odejmowanie wartości od liczby nominałów
    def coins(self, value):
        try:
            if(self.number_of_nominals<1):
                raise BelowZeroNumberOfNominals
        except BelowZeroNumberOfNominals:
            messagebox.showinfo(parent=self.window2, title="UWAGA",
                                message="Wrzucono już podaną na początku liczbę monet.")
        else:
            self.number_of_nominals -= 1
            machine.add_coin(value)
            self.text_print(1)

    #sprawdzanie czy wprowadzona liczba nominałów jest większa od 0 i dodatnia, ustawienie tej liczby
    def number_of_nominal(self,entry_1):
        try:
            self.number_of_nominals = int(self.window2.entry_1.get())
            if self.number_of_nominals<1:
                raise NumberOfNominalsNotInteger
        except NumberOfNominalsNotInteger:
            messagebox.showerror(parent = self.window2, title = "UWAGA", message="Podaj dodatnią,całkowitą liczbę monet.")
        except ValueError:
            messagebox.showerror(parent=self.window2, title="UWAGA", message="Podaj dodatnią,całkowitą liczbę monet.")
        else:
            messagebox.showinfo(parent=self.window2, title="INFO", message="Zmiana ilości nominałów.\n"
                                                                           "Jeśli jakieś pieniądze zostały wrzucone,\n"
                                                                           "to zostaną zwrócone.")
            machine.add_number_nominals(self.number_of_nominals)
            self.text_print(1)

    #dodawanie/usuwanie biletów w zależności od flagi
    def add_del(self, value, flag):
        if flag == 1:
            ticket.addTickets(value)
        if flag == 0:
            ticket.delTicket(value)
        if (value == 280):
            self.text_frame[0].delete(0.0, END)
            self.text_frame[0].insert(0.0, str(ticket.buy_ticket[value]))
        if (value == 140):
            self.text_frame[1].delete(0.0, END)
            self.text_frame[1].insert(0.0, str(ticket.buy_ticket[value]))
        if (value == 380):
            self.text_frame[2].delete(0.0, END)
            self.text_frame[2].insert(0.0, str(ticket.buy_ticket[value]))
        if (value == 190):
            self.text_frame[3].delete(0.0, END)
            self.text_frame[3].insert(0.0, str(ticket.buy_ticket[value]))
        if (value == 500):
            self.text_frame[4].delete(0.0, END)
            self.text_frame[4].insert(0.0, str(ticket.buy_ticket[value]))
        if (value == 250):
            self.text_frame[5].delete(0.0, END)
            self.text_frame[5].insert(0.0, str(ticket.buy_ticket[value]))

        self.text_print(0)

    #pętla odpowiedzialna za płacenie groszami
    def pay_1_100_times(self):
        if self.number_of_nominals>=100:
            for g in range(100):
                self.coins(1)

    #funkcja działająca na sam koniec, zerująca wszystko
    def finish_function(self):
        ticket.amount_ticket = 0
        ticket.list_ticket = []
        ticket.buy_ticket = {x: 0 for x in ticket.tickets}
        machine.throw_coin = {x: 0 for x in Coin.coins}
        machine.list_coins = []
        machine.i = 0
        machine.amount_coins = 0
        self.release_coins = {x: 0 for x in Coin.coins}
        self.number_of_nominals = 1
        self.return_to_ticket()
        self.text_amount.delete(0.0, END)
        self.text_amount.insert(0.0, "Do zapłaty: 0.0 zł")
        for i in range(6):
            self.text_frame[i].delete(0.0, END)
            self.text_frame[i].insert(0.0, 0)

    # wyświetlanie paragonu przy zapłacie kartą
    def show_everything2(self):
        self.look = 0
        string = "Bilety zostaną wydrukowane.\n\n"
        string += "Kupione bilety: "
        for x in ticket.buy_ticket:
            if ticket.buy_ticket[x] > 0:
                self.look += 1
                if (self.look % 3 == 0):
                    string += "\n"
                string += str(ticket.buy_ticket[x]) + " x "
                string += str(x / 100) + "zł,"
                string += " "
        string += "\nDo zapłaty: " + str(ticket.amount_ticket) + "zł.\n"
        string += "Zapłacono kartą.\n"
        string += "Jeśli wrzucono jakieś pieniądze do automatu,\n"
        string += "to zostaną zwrócone."
        string += "\n\nZapraszamy ponownie."
        return string

    #wyświetlanie paragonu przy zapłacie pieniędzmi
    def show_everything(self,flag):
        self.look=0
        string = "Bilety zostaną wydrukowane.\n\n"
        string +="Kupione bilety: "
        for x in ticket.buy_ticket:
            if ticket.buy_ticket[x]>0:
                self.look+=1
                if(self.look%3==0):
                    string +="\n"
                string += str(ticket.buy_ticket[x]) + " x "
                string += str(x / 100) + "zł,"
                string += " "
        string += "\nDo zapłaty: " + str(ticket.amount_ticket) + "zł.\n"
        string += "Wrzucono: " + str(machine.amount_coins) + "zł.\n"
        string += "Reszta: " + str(self.change2/100) + "zł\n"
        if (flag == 1):
            self.look=0
            string += "Automat wydał: "
            for x in self.release_coins:
                if self.release_coins[x] > 0:
                    self.look+=1
                    if (self.look % 3 == 0):
                        string += "\n"
                    string += str(self.release_coins[x]) + " x "
                    string += str(x / 100) + "zł,"
                    string += " "
        string += "\n\nZapraszamy ponownie."
        return string

    #zapłata kartą
    def pay_via_card(self):
        windowNew = Tk()
        windowNew.geometry("350x250+260+150")
        windowNew.title("RESZTA")
        windowNew.resizable(0, 0)
        for x in (5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1):
            machine.inside_machine[x] = machine.inside_machine[x] - machine.throw_coin[x]
        Label(master=windowNew, text= self.show_everything2(), font=("Arial", 10)).pack()
        self.finish_function()
        print("\nWRZUCONE PO: ", machine.throw_coin)
        print("AUTOMAT PO:  ", machine.inside_machine)

    #zapłata pieniędzmi
    def pay_for_ticket(self):
        try:
            if machine.amount_coins <= 0:
                raise ThrowZeroMoney
            if self.number_of_nominals != 0:
                raise NotZeroNumberOfNominals
        except ThrowZeroMoney:
            messagebox.showerror(parent = self.window2, title="UWAGA",
                                 message="Musisz wrzucić jakieś pieniądze!")
        except NotZeroNumberOfNominals:
            messagebox.showerror(parent=self.window2, title="UWAGA",
                                 message="Nie wrzucono pełnej liczby podanych monet!")
        else:
            try:
                self.change = (machine.amount_coins - ticket.amount_ticket)*100.0
                self.change = round(self.change,2) #problem z zaokrąglaniem
                self.change2 = self.change
                if self.change < 0:
                    raise ToLittleCash
            except ToLittleCash:
                messagebox.showerror(parent=self.window2, title="UWAGA",
                                     message="Wrzucono za mało pieniędzy!")
            else:
                if self.change == 0:
                    windowNew = Tk()
                    windowNew.geometry("350x250+260+150")
                    windowNew.title("RESZTA")
                    windowNew.resizable(0, 0)
                    Label(master=windowNew, text=self.show_everything(0), font=("Arial", 10)).pack()
                    self.finish_function()
                    print("\nWRZUCONE PO: ", machine.throw_coin)
                    print("AUTOMAT PO:  ", machine.inside_machine)

                elif self.change > 0:
                    for x in (5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1):
                        self.back_from_automat_coins[x] = machine.inside_machine[x]

                    for x in (5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1):
                        while (self.back_from_automat_coins[x] > 0) and (x <= self.change):
                            self.change = self.change - x
                            self.release_coins[x] += 1
                            self.back_from_automat_coins[x] -= 1
                            if self.change == 0:
                                break
                    print("WYDANE:   ", self.release_coins)

                    if self.change == 0:
                        windowNew = Tk()
                        windowNew.title("RESZTA")
                        windowNew.geometry("350x250+260+150")
                        windowNew.resizable(0, 0)
                        Label(master = windowNew, text=self.show_everything(1), font=("Arial", 10)).pack()
                        self.finish_function()
                        for x in (5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1):
                            machine.inside_machine[x] = self.back_from_automat_coins[x]
                        print("\nWRZUCONE PO: ", machine.throw_coin)
                        print("AUTOMAT PO:  ", machine.inside_machine)

                    else:
                        messagebox.showerror(parent= self.window2,title="UWAGA",
                                             message="Tylko odliczona kwota!\n"
                                                     "Automat nie ma jak wydać monet.\n"
                                                     "Zwracam pieniądze.")

                        for x in (5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1):
                            machine.inside_machine[x] = machine.inside_machine[x] - machine.throw_coin[x]
                        self.finish_function()
                        print("\nWRZUCONE PO: ", machine.throw_coin)
                        print("AUTOMAT PO:  ", machine.inside_machine)

    def create_new_window(self):
      try:
         if ticket.amount_ticket <= 0:
            raise NotAnyTicket
      except NotAnyTicket:
            messagebox.showerror(title="UWAGA",
                                 message="Musisz wybrać co najmniej jeden bilet!")
      else:
        for i in range(6):
            self.text_frame[i].config(state=DISABLED)
            self.button_p_tab[i].config(state=DISABLED)
            self.button_m_tab[i].config(state=DISABLED)
        self.button_pay_1.config(state=DISABLED)

        #tworzenie nowego okienka do zapłaty
        self.window2 = Toplevel()
        self.window2.geometry("820x450+260+150")
        self.window2.resizable(width=False, height=False)
        self.window2.title("Zaplata")
        self.window2.photo = []

        #wszystkie etykiety
        Label(master=self.window2, height=25, width=65, bg='grey').place(x=350, y=50)
        Label(master=self.window2, text="Wybierz nominał:", font=("Arial", 22)).place(x=465, y=10)
        Label(master=self.window2, text="Liczba nominałów:", font=("Arial", 15)).place(x=20, y=100)

        #wczytanie zdjęć i dodanie do przyciskow z banknotami
        for i in range(12):
            self.window2.photo.append(PhotoImage(master=self.window2, file="images/"+str(i)+".png"))
        Button(master=self.window2,image=self.window2.photo[0],command=lambda: self.coins(1)).place(x=370,y=70)
        Button(master=self.window2,image=self.window2.photo[1],command=lambda: self.coins(2)).place(x=460,y=70)
        Button(master=self.window2,image=self.window2.photo[2],command=lambda: self.coins(5)).place(x=550,y=70)
        Button(master=self.window2,image=self.window2.photo[3],command=lambda: self.coins(10)).place(x=640,y=70)
        Button(master=self.window2,image=self.window2.photo[4],command=lambda: self.coins(20)).place(x=730,y=70)
        Button(master=self.window2,image=self.window2.photo[5],command=lambda: self.coins(50)).place(x=400,y=160)
        Button(master=self.window2,image=self.window2.photo[6],command=lambda: self.coins(100)).place(x=500,y=160)
        Button(master=self.window2,image=self.window2.photo[7],command=lambda: self.coins(200)).place(x=600,y=160)
        Button(master=self.window2,image=self.window2.photo[8],command=lambda: self.coins(500)).place(x=700,y=160)
        Button(master=self.window2,image=self.window2.photo[9],command=lambda: self.coins(1000)).place(x=400,y=250)
        Button(master=self.window2,image=self.window2.photo[10],command=lambda: self.coins(2000)).place(x=600,y=250)
        Button(master=self.window2,image=self.window2.photo[11],command=lambda: self.coins(5000)).place(x=500,y=340)

        #pozostałe przyciski
        Button(master=self.window2, text="Wybierz kolejny bilet", width=20, height=3, bg='green',
               command=self.return_to_ticket).place(x=20, y=356)
        Button(master=self.window2, text="OK", width=5, height=2,bg='green',
               command=lambda:self.number_of_nominal(self.window2.entry_1)).place(x=275, y=93)
        Button(master=self.window2, text="Wpłać 1 zł po groszu", width=20, height=3, bg='grey',
               command=lambda: self.pay_1_100_times()).place(x=180, y=356)
        Button(master=self.window2, text="Zapłać pieniędzmi", width=20, height=3, bg='green',
               command=lambda: self.pay_for_ticket()).place(x=180, y=285)
        Button(master=self.window2, text="Zapłać kartą", width=20, height=3, bg='green',
               command=lambda: self.pay_via_card()).place(x=20, y=285)

        #wyswietlanie tekstu
        self.window2.text = Text(master=self.window2, width=19, height=3, padx=10, pady=10, font=("Arial", 20))
        self.window2.text.place(x=20, y=150)
        self.window2.text.insert(0.0,    "Do zapłaty: " + str(ticket.amount_ticket) + " zł\n")
        self.window2.text.insert(CURRENT,"Wrzucono:  " + str(machine.amount_coins) + " zł\n")
        self.window2.text.insert(END, "Liczba nominałów: " + str(self.number_of_nominals))

        #wprowadzanie liczby nominałów
        self.window2.entry_1 = Entry(master=self.window2, width=3, font=("Arial", 20))
        self.window2.entry_1.place(x=200, y=97)

        self.window2.mainloop()

    def create_widgets(self):
        #dodawanie biletów
        self.button_p1 = Button(text="Bilet normalny 20 min\n2,80zł", width=20, height=5,bg='grey',state=NORMAL,
                               command=lambda: self.add_del(280,1))
        self.button_p2 = Button(text='Bilet ulgowy 20 min\n1,40zł', width=20, height=5, bg='grey',state=NORMAL,
                               command=lambda: self.add_del(140,1))
        self.button_p3 = Button(text="Bilet normalny 40 min\n3,80zł", width=20, height=5,bg='grey',state=NORMAL,
                               command=lambda: self.add_del(380,1))
        self.button_p4 = Button(text='Bilet ulgowy 40 min\n1,90zł', width=20, height=5,bg='grey',state=NORMAL,
                               command=lambda: self.add_del(190,1))
        self.button_p5 = Button(text="Bilet normalny 60 min\n5,00zł", width=20, height=5,bg='grey',state=NORMAL,
                               command=lambda: self.add_del(500,1))
        self.button_p6 = Button(text="Bilet ulgowy 60 min\n2,50zł", width=20, height=5,bg='grey',state=NORMAL,
                               command=lambda: self.add_del(250,1))
        self.button_p_tab = [self.button_p1, self.button_p2, self.button_p3, self.button_p4, self.button_p5,
                             self.button_p6]
        self.button_p1.place(x=50, y=70)
        self.button_p2.place(x=450, y=70)
        self.button_p3.place(x=50,y=170)
        self.button_p4.place(x=450,y=170)
        self.button_p5.place(x=50,y=270)
        self.button_p6.place(x=450,y=270)

        #odejmowanie biletów
        self.button_m1 = Button(text="x", width=4, height=2, bg='red', state=NORMAL,
                                command=lambda: self.add_del(280, 0))
        self.button_m2 = Button(text="x", width=4, height=2, bg='red', state=NORMAL,
                                command=lambda: self.add_del(140, 0))
        self.button_m3 = Button(text="x", width=4, height=2, bg='red', state=NORMAL,
                                command=lambda: self.add_del(380, 0))
        self.button_m4 = Button(text="x", width=4, height=2, bg='red', state=NORMAL,
                                command=lambda: self.add_del(190, 0))
        self.button_m5 = Button(text="x", width=4, height=2, bg='red', state=NORMAL,
                                command=lambda: self.add_del(500, 0))
        self.button_m6 = Button(text="x", width=4, height=2, bg='red', state=NORMAL,
                                command=lambda: self.add_del(250, 0))
        self.button_m_tab = [self.button_m1, self.button_m2, self.button_m3, self.button_m4, self.button_m5,
                             self.button_m6]
        self.button_m1.place(x=300, y=90)
        self.button_m2.place(x=700, y=90)
        self.button_m3.place(x=300, y=190)
        self.button_m4.place(x=700, y=190)
        self.button_m5.place(x=300, y=290)
        self.button_m6.place(x=700, y=290)

        #wyświetlanie tekstu
        for i in range (6):
            self.text_frame.append(Text(width=2, height=0,font=("Arial",30),pady=6,padx=6,state=NORMAL))
            self.text_frame[i].insert(0.0, 0)
        self.text_frame[0].place(x=225, y=80)
        self.text_frame[1].place(x=625, y=80)
        self.text_frame[2].place(x=225, y=180)
        self.text_frame[3].place(x=625, y=180)
        self.text_frame[4].place(x=225, y=280)
        self.text_frame[5].place(x=625, y=280)

        # etykieta, przyciski zapłać i do zapłaty
        Label(text="Wybierz ilość i rodzaj biletów:", font=("Arial", 22)).place(x=200, y=10)
        self.button_pay_1=Button(text="Zapłać",width=20,height=3,bg='green',command= lambda: self.create_new_window())
        self.button_pay_1.place(x=415, y=380)
        self.text_amount = Text(width=15, height=0, font=("Arial", 15), pady=6, padx=6, state=NORMAL)
        self.text_amount.place(x=200, y=390)
        self.text_amount.insert(0.0, "Do zapłaty: 0.0 zł")

