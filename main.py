from tkinter import *
from tkinter import messagebox
from window import Window

def main():

    try:
        root = Tk()
        window = Window(root)
        root.resizable(width=False, height=False)
        root.mainloop()

    except:
        messagebox.showerror("BŁĄD!", "Błąd przy tworzeniu aplikacji")

if __name__ == "__main__":
    main()


