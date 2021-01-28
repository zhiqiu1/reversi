class Reversi:
    def __init__(self, row: int, col: int):
        self.board = [['.' for _ in range(col)] for _ in range(row)]
        self.board[row // 2 - 1][col // 2 - 1], self.board[row // 2 - 1][col // 2] = "W", "B"
        self.board[row // 2][col // 2 - 1], self.board[row // 2][col // 2] = "B", "W"
        self.N_OF_ROW, self.N_OF_COL = row, col
        self.curr_turn, self.next_turn = "B", "W"
        self.disk_count = {"B": 2, "W": 2}
        self._DIRECTIONS = {(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)}
        self.game_is_over = False

    def place(self, move: tuple, reached_bottom_node=False):
        # This function should be called only if is_valid_move(move) returns True
        # Reached_bottom_node is for time saving when building bottom nodes of minimax tree
        for i, j in self._DIRECTIONS:
            temp_row, temp_col = move[0], move[1]
            if self._disk_is_within_board_and_on_the_position(temp_row + i, temp_col + j, self.next_turn):
                disks_to_flip = set()
                while self._disk_is_within_board_and_on_the_position(temp_row + i, temp_col + j, self.next_turn):
                    temp_row += i
                    temp_col += j
                    disks_to_flip.add((temp_row, temp_col))
                if self._disk_is_within_board_and_on_the_position(temp_row + i, temp_col + j, self.curr_turn):
                    for i, j in disks_to_flip:
                        self.board[i][j] = self.curr_turn
                        self.disk_count[self.curr_turn] += 1
                        self.disk_count[self.next_turn] -= 1
        self.board[move[0]][move[1]] = self.curr_turn
        self.disk_count[self.curr_turn] += 1
        self.curr_turn, self.next_turn = self.next_turn, self.curr_turn
        if not reached_bottom_node:
            self._game_over()

    def _disk_is_within_board_and_on_the_position(self, temp_row: int, temp_col: int, color: str) -> bool:
        return 0 <= temp_row < self.N_OF_ROW and 0 <= temp_col < self.N_OF_COL \
               and self.board[temp_row][temp_col] == color

    def is_valid_move(self, move: tuple) -> bool:
        if self.board[move[0]][move[1]] == '.':
            for i, j in self._DIRECTIONS:
                temp_row, temp_col = move[0], move[1]
                if self._disk_is_within_board_and_on_the_position(temp_row + i, temp_col + j, self.next_turn):
                    while self._disk_is_within_board_and_on_the_position(temp_row + i, temp_col + j, self.next_turn):
                        temp_row += i
                        temp_col += j
                    if self._disk_is_within_board_and_on_the_position(temp_row + i, temp_col + j, self.curr_turn):
                        return True
        return False

    def _game_over(self):
        if self.disk_count["B"] + self.disk_count["W"] == self.N_OF_ROW * self.N_OF_COL:
            self.game_is_over = True
            return
        for i in range(self.N_OF_ROW):
            for j in range(self.N_OF_COL):
                if self.is_valid_move((i, j)):
                    return
        self.game_is_over = True
