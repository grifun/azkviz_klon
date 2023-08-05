import tk_game
import tk_admin
from queue import Queue

class HEXAGON:
    def __init__(self, idx):
        self.idx = idx
        self.state = "white"
        self.neighbors =[]
        
        self.left_wall = False
        self.right_wall = False
        self.bottom_wall = False
    def set_state(self, state):
        self.state = state

class QUESTION:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.abbreviation = [ word.upper()[0] for word in answer.split() ]


class GAME:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.rows = 7
        self.prepare_hexagons( self.rows )
        self.finished = False
        self.questions = [ QUESTION("Legenda Holešovic?","Jirka Kára") ]
        self.question_outcome = None
        self.hexagon_idx_opened = -1

    def prepare_hexagons(self, rows):
        idx = 0
        self.hexagons = []
        for row in range(rows+1):
            for col in range(row):
                h = HEXAGON(idx)
                if col == 0:
                    h.left_wall = True
                else:
                    h.neighbors.append(idx-1)
                    self.hexagons[idx-1].neighbors.append(idx)
                if col == row-1:
                    h.right_wall = True
                if row == rows:
                    h.bottom_wall = True
                # vertical neighbors:
                if row != 0: 
                    if col != row-1: #not right one
                        h.neighbors.append(idx-row+1)
                        self.hexagons[idx-row+1].neighbors.append(idx)
                    if col != 0: #not left one
                        h.neighbors.append(idx-row)
                        self.hexagons[idx-row].neighbors.append(idx)
                self.hexagons.append(h)
                idx += 1
        
        print("hexagons prepared like this:")
        for hexagon in self.hexagons:
            print("hexagon idx ", hexagon.idx)
            print(hexagon.neighbors)

    def set_windows(self, admin_window, game_window):
        self.admin_window = admin_window
        self.game_window = game_window

    def set_players(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        
        self.game_window.redraw()
        self.admin_window.clear()

    def exit(self):
        self.admin_window.exit()
        self.game_window.exit()
        exit(0)

    def hexagon_clicked(self, idx):
        print("clicked hexagon: ", idx)
        if self.hexagons[idx].state == "white" or self.hexagons[idx].state == "black":
            self.ask_question(idx, self.questions[0]) 

    def set_question_outcome(self, outcome):
        self.question_outcome = outcome
        self.hexagons[self.hexagon_idx_opened].set_state( self.question_outcome )
        self.game_window.redraw()
        self.admin_window.clear()
        self.check_finnish()

    def ask_question(self, idx, question):
        print("asking question")
        self.question_outcome = None
        self.hexagon_idx_opened = idx
        self.admin_window.show_question(question.question, question.answer)
        self.game_window.show_question(question.abbreviation)

    def start_timer(self):
        self.game_window.start_timer()

    def bfs(self, player, bfs_list):
        print("dostavam bfs s ", bfs_list)
        Q = Queue()

        while True:
            if Q.empty():
                print("restartuju bfs s ", bfs_list)
                node = self.hexagons[ bfs_list[0] ]
                print("new node = ", node.idx)
                bfs_list.remove(node.idx)
                state = [False,False,False]
                closed_list = [node.idx]
            else:
                node = Q.get()
                print("opening node = ", node.idx)
                if node.idx in closed_list:
                    continue
                bfs_list.remove(node.idx)
                closed_list.append(node.idx)

            if node.left_wall:
                state[0] = True
            if node.right_wall:
                state[1] = True
            if node.bottom_wall:
                state[2] = True

            for neighbor_idx in node.neighbors:
                new_node = self.hexagons[neighbor_idx]
                if new_node.state == player:
                    Q.put(new_node)

            if sum(state) == 3:
                print("vracim true")
                return True

            if len(bfs_list) == 0:
                print("vracim false")
                return False
        


    def check_finnish(self):
        blue_indexes = [ h.idx for h in self.hexagons if h.state == "blue" ]
        orange_indexes = [ h.idx for h in self.hexagons if h.state == "orange" ]
        
        if len( blue_indexes ) >= self.rows:
            blue_status = self.bfs( "blue", blue_indexes )
            if blue_status:
                self.blue_wins()
        
        if len( orange_indexes ) >= self.rows:
            orange_status = self.bfs( "orange", orange_indexes )
            if orange_status:
                self.orange_wins()
        
    def blue_wins(self):
        self.game_window.blue_wins()

    def orange_wins(self):
        self.game_window.orange_wins()
        
    
game = GAME("Hráč 1", "Hráč 2")
game_window = tk_game.GAME_WINDOW(game)

admin_window = tk_admin.ADMIN_WINDOW(game)
admin_window.get_players()


game.set_windows(admin_window, game_window)

admin_window.show()
print("jsem tady")