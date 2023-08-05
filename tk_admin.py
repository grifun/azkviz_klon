import tkinter as tk

class ADMIN_WINDOW:
    def __init__(self, game):
        self.game = game
        self.width = 800
        self.height = 600

        self.window = tk.Tk()
        self.window.geometry(str(self.width)+"x"+str(self.height))
        self.window.title("AZKvíz admin")

        #self.window.mainloop()

    def get_players(self):
        self.clear()
        player1_label = tk.Label(self.window, text="Jméno prvního soutěžícího", width=400, font="Times 25 bold")
        player1_window  = tk.Entry(self.window)
        player2_label = tk.Label(self.window, text="Jméno druhého soutěžícího", width=400, font="Times 25 bold")
        player2_window  = tk.Entry(self.window)
        b1 = tk.Button(self.window, text = "Nastavit", bg="BLUE", width=100, font="Times 25 bold", command = lambda:self.game.set_players(player1_window.get(), player2_window.get()))
        player1_label.pack()
        player1_window.pack()
        player2_label.pack()
        player2_window.pack()
        b1.pack()

    def show(self):
        self.window.mainloop()
        return self.outcome

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        close_button = tk.Button(self.window, text="Zavřít", bg="GRAY", width=100, font="Times 25 bold", command = lambda:self.game.exit())
        close_button.pack()

    def exit(self):
        self.window.destroy()

    def show_question(self, question, answer):
        self.clear()
        question_title = tk.Label(self.window, text="Otázka:", font="Times 25 bold")
        question_label = tk.Label(self.window, text=question, font="Times 25 bold")
        empty_label = tk.Label(self.window, text=" ", font="Times 25 bold")
        answer_title = tk.Label(self.window, text="Odpověď:", font="Times 25 bold")
        answer_label = tk.Label(self.window, text=answer, font="Times 25 bold")

        b_timer = tk.Button(self.window, text="Odpočet", width=100, font="Times 25 bold", command = lambda:self.game.start_timer() )
        b_blue = tk.Button(self.window, text=self.game.player1, bg="BLUE", width=100, font="Times 25 bold", command = lambda:self.game.set_question_outcome("blue"))
        b_orange = tk.Button(self.window, text=self.game.player2, bg="ORANGE", width=100, font="Times 25 bold", command = lambda:self.game.set_question_outcome("orange"))
        b_black = tk.Button(self.window, text="nikdo", fg="WHITE", bg="BLACK", width=100, font="Times 25 bold", command = lambda:self.game.set_question_outcome("black"))
        
        question_title.pack()
        question_label.pack()
        empty_label.pack()
        answer_title.pack()
        answer_label.pack()
        
        b_timer.pack()
        b_blue.pack()
        b_orange.pack()
        b_black.pack()

