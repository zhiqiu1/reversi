from tkinter import *

import game_ai
import game_mechanics


class UI:
    def __init__(self):
        self._ui = Tk()
        self._ui.title('Reversi')
        self._entry_boxes()
        self._ui.mainloop()

    def _entry_boxes(self):
        self._n_of_row_var = IntVar(value=8)
        Label(self._ui, text='Number of rows\n(An EVEN NUMBER that is >= 4)').pack()
        Entry(self._ui, text=self._n_of_row_var, width=10).pack()

        self._n_of_col_var = IntVar(value=8)
        Label(self._ui, text='Number of columns\n(An EVEN NUMBER that is >= 4').pack()
        Entry(self._ui, text=self._n_of_col_var, width=10).pack()

        self._player_color = StringVar(value='B')
        Label(self._ui, text='Your color\n(B or W. B goes first)').pack()
        Entry(self._ui, text=self._player_color, width=10).pack()

        self.search_depth = IntVar(value=3)
        Label(self._ui, text='AI search depth\n(Quick match for 8*8 board: 1-6)').pack()
        Entry(self._ui, text=self.search_depth, width=10).pack()

        Label(self._ui, text='\nNote: the game ends if the player who takes the turn has no valid move.').pack()
        Button(self._ui, text='START', width=20, height=3, command=self.game_start).pack()

    def game_start(self):
        self._n_of_row = self._n_of_row_var.get();
        self._n_of_col = self._n_of_col_var.get();
        self._player_color = self._player_color.get()
        self.search_depth = self.search_depth.get()
        self.game = game_mechanics.Reversi(self._n_of_row, self._n_of_col)

        # Draw the board and its lines
        for widget in self._ui.winfo_children():
            widget.destroy()
        self._canvas = Canvas(master=self._ui, width=100 * self._n_of_col, height=100 * self._n_of_row,
                              background='green')
        self._canvas.pack()
        for i in range(self._n_of_row):
            self._canvas.create_line(0, i * 100, self._n_of_row * 100, i * 100, fill='black')
        for i in range(self._n_of_col):
            self._canvas.create_line(i * 100, 0, i * 100, self._n_of_col * 100, fill='black')
        self._canvas.bind('<Button-1>', self._move)

        # Game status
        self._status_label = Label(self._ui)
        self._status_label.pack()
        self._b_disk_count_label = Label(self._ui, text='B: ' + str(self.game.disk_count["B"]))
        self._b_disk_count_label.pack()
        self._w_disk_count_label = Label(self._ui, text='W: ' + str(self.game.disk_count["W"]))
        self._w_disk_count_label.pack()
        Button(self._ui, text='Start a new game', width=20, height=3, command=self._entry_boxes).pack()

        # Draw the disks. AI takes the move if it goes first.
        self._place_and_draw_the_board_and_check_game_over(None if self._player_color == 'B'
                                                           else game_ai.AI(self.game, self.search_depth).MOVE)

        # Code for AI against AI. Setting both AIs' search depth to 4 in an 8x8 board will create a interesting shape.
        # while not self.game.game_is_over:
        #     self._place_and_draw_the_board_and_check_game_over(game_ai.AI(self.game, 4).MOVE)
        #     if not self.game.game_is_over:
        #         self._place_and_draw_the_board_and_check_game_over(game_ai.AI(self.game, 4).MOVE)

    def _move(self, event):
        x = divmod(event.x, 100)[0]
        y = divmod(event.y, 100)[0]
        if self.game.is_valid_move((y, x)):
            self._place_and_draw_the_board_and_check_game_over((y, x))
            if not self.game.game_is_over:
                self._place_and_draw_the_board_and_check_game_over(game_ai.AI(self.game, self.search_depth).MOVE)

    def _place_and_draw_the_board_and_check_game_over(self, move=None):
        # place
        if move:
            self.game.place(move)

        # draw_the_board
        for i in range(self._n_of_row):
            for j in range(self._n_of_col):
                if self.game.board[i][j] == 'B':
                    self._canvas.create_oval(10 + j * 100, 10 + i * 100, (j + 1) * 100 - 10, (i + 1) * 100 - 10,
                                             fill='black')
                elif self.game.board[i][j] == 'W':
                    self._canvas.create_oval(10 + j * 100, 10 + i * 100, (j + 1) * 100 - 10, (i + 1) * 100 - 10,
                                             fill='white')
        # Draw a red dot on the last move
        if move:
            self._canvas.create_oval(45 + (move[1]) * 100, 45 + (move[0]) * 100, (move[1] + 1) * 100 - 45,
                                     (move[0] + 1) * 100 - 45, fill='red')
        self._b_disk_count_label.configure(text='B: ' + str(self.game.disk_count["B"]))
        self._w_disk_count_label.configure(text='W: ' + str(self.game.disk_count["W"]))

        # check_game_over
        if self.game.game_is_over:
            self._status_label.configure(
                text='WINNER: B' if self.game.disk_count["W"] < self.game.disk_count["B"]
                else 'WINNER: W' if self.game.disk_count["W"] > self.game.disk_count["B"] else 'WINNER: NONE',
                font=("arial", 20))
        else:
            self._status_label.configure(
                text="Your Turn" if self.game.curr_turn == self._player_color else "AI is thinking")
        self._ui.update()
